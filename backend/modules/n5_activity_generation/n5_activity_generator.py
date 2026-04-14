import json
import logging
from typing import List, Dict, Any

# Import database mẫu từ module riêng
from backend.modules.n5_activity_generation.n5_activity_templates import ACTIVITY_TEMPLATES

# Import module LLM cho hybrid approach
# Nếu import thất bại (thiếu dependency), hệ thống vẫn hoạt động bình thường với rule-based
try:
    from backend.modules.n5_activity_generation.n5_llm_generator import (
        generate_activities_from_llm,
        _is_llm_available,
    )
    LLM_MODULE_AVAILABLE = True
except ImportError:
    LLM_MODULE_AVAILABLE = False

logger = logging.getLogger(__name__)


# ==================== SCORING WEIGHTS ====================
SCORING_WEIGHTS = {
    "tag_overlap":       0.35,   # Trùng tag trực tiếp giữa user và activity
    "location_synergy":  0.15,   # Location-level tag cũng phù hợp với user
    "cost_efficiency":   0.20,   # Chi phí hợp lý so với ngân sách
    "time_fit":          0.15,   # Thời gian phù hợp với giới hạn ngày
    "diversity_bonus":   0.15,   # Thưởng cho hoạt động thuộc nhóm tag khác biệt
}

DEFAULT_CONSTRAINTS = {
    "budget": 10_000_000,               # Tổng ngân sách (VNĐ)
    "max_cost_per_activity": None,       # None = tự tính từ budget
    "min_cost_per_activity": 0,          # Lọc hoạt động quá rẻ / không phù hợp
    "max_time_per_day": 480,             # phút (8 giờ)
    "max_time_per_activity": 300,        # phút (5 giờ)
    "min_match_score": 0.1,              # Bỏ hoạt động có điểm quá thấp
    "exclude_tags": [],                  # Tag user không muốn
    "max_activities": 12,                # Giới hạn kết quả
    "prefer_unique_categories": True,    # Ưu tiên đa dạng loại hoạt động
}


def _merge_constraints(user_constraints: Dict[str, Any] | None) -> Dict[str, Any]:
    """Gộp constraints người dùng với giá trị mặc định."""
    merged = {**DEFAULT_CONSTRAINTS}
    if user_constraints:
        merged.update(user_constraints)

    # Tự tính max_cost nếu chưa set (tối đa 30 % ngân sách cho 1 activity)
    if merged["max_cost_per_activity"] is None:
        merged["max_cost_per_activity"] = merged["budget"] * 0.30
    return merged


def _passes_constraints(act: Dict, constraints: Dict[str, Any]) -> tuple[bool, str | None]:
    """
    Kiểm tra activity có vượt qua tất cả ràng buộc không.
    Returns (passed: bool, rejection_reason: str | None).
    """
    cost = act["cost"]
    time = act["time"]

    # --- Chi phí ---
    if cost > constraints["max_cost_per_activity"]:
        return False, f"Chi phí {cost:,}đ vượt giới hạn {constraints['max_cost_per_activity']:,.0f}đ/hoạt động"
    if cost < constraints["min_cost_per_activity"]:
        return False, f"Chi phí {cost:,}đ dưới mức tối thiểu {constraints['min_cost_per_activity']:,}đ"

    # --- Thời gian ---
    if time > constraints["max_time_per_activity"]:
        return False, f"Thời gian {time} phút vượt giới hạn {constraints['max_time_per_activity']} phút/hoạt động"
    if time > constraints["max_time_per_day"]:
        return False, f"Thời gian {time} phút vượt giới hạn {constraints['max_time_per_day']} phút/ngày"

    # --- Exclude tags ---
    excluded = set(constraints.get("exclude_tags", []))
    act_tags = set(act["tags"])
    overlap_excluded = act_tags & excluded
    if overlap_excluded:
        return False, f"Chứa tag bị loại: {', '.join(overlap_excluded)}"

    return True, None


def _compute_match_score(
    act: Dict,
    user_tags: List[str],
    location_tags: List[str],
    constraints: Dict[str, Any],
    seen_tag_groups: set,
    location_score: float = 1.0,  # Điểm từ N4 (ranking score của location)
) -> tuple[float, List[str]]:
    """
    Tính match_score (0.0 – 1.0) theo nhiều chiều và trả về danh sách reasons.
    
    === CÁCH TÍNH N5 MATCH_SCORE ===
    N5 nhận locations từ N4 (Location Ranking), mỗi location có:
      - location_id: ID định danh
      - name: Tên địa điểm (VD: "Sa Pa", "Phú Quốc")
      - score: Ranking score từ N4 (0-1, phản ánh mức độ phù hợp từ N4)
      - metadata: Mô tả, tags của N4
      - vector: Vector embedding từ N4
    
    N5 match_score kết hợp 6 nhân tố:
      1. tag_overlap: Trùng tag trực tiếp giữa user và activity (weight: 0.35)
      2. location_synergy: Location-level tag phù hợp (weight: 0.15)
      3. cost_efficiency: Chi phí hợp lý (weight: 0.20)
      4. time_fit: Thời gian vừa vặn (weight: 0.15)
      5. diversity_bonus: Thưởng cho đa dạng loại hoạt động (weight: 0.15)
      6. location_score: Điểm từ N4 tích hợp vào (được nhân vào điểm cuối)
    
    Công thức: final_score = (weighted_sum) * location_score
      → Điểm từ N4 được sử dụng để hiệu chỉnh điểm cuối: location nào cao hơn sẽ
        có activities với điểm tối ưu lớn hơn.
    """
    user_tag_set = set(user_tags)
    act_tag_set = set(act["tags"])
    loc_tag_set = set(location_tags)
    reasons: List[str] = []

    # ---------- 1. Tag Overlap (0 – 1) ----------
    direct_match = user_tag_set & act_tag_set
    if user_tags:
        tag_overlap = len(direct_match) / len(user_tag_set)
    else:
        tag_overlap = 0.0
    if direct_match:
        reasons.append(f"Trùng sở thích: {', '.join(sorted(direct_match))}")

    # ---------- 2. Location Synergy (0 – 1) ----------
    loc_user_match = user_tag_set & loc_tag_set
    if user_tags:
        location_synergy = len(loc_user_match) / len(user_tag_set)
    else:
        location_synergy = 0.0
    if loc_user_match:
        reasons.append(f"Địa điểm phù hợp phong cách: {', '.join(sorted(loc_user_match))}")

    # ---------- 3. Cost Efficiency (0 – 1) ----------
    max_cost = constraints["max_cost_per_activity"]
    if max_cost > 0:
        # Hoạt động dùng 30-70 % ngưỡng chi phí → điểm cao nhất
        ratio = act["cost"] / max_cost
        if ratio <= 0.7:
            cost_score = 1.0
        elif ratio <= 1.0:
            cost_score = 1.0 - (ratio - 0.7) / 0.3   # giảm tuyến tính 1→0
        else:
            cost_score = 0.0
    else:
        cost_score = 0.5

    if cost_score >= 0.7:
        reasons.append(f"Chi phí hợp lý ({act['cost']:,}đ)")
    elif cost_score >= 0.4:
        reasons.append(f"Chi phí ở mức trung bình ({act['cost']:,}đ)")

    # ---------- 4. Time Fit (0 – 1) ----------
    max_time = constraints["max_time_per_day"]
    if max_time > 0:
        time_ratio = act["time"] / max_time
        if time_ratio <= 0.5:
            time_score = 1.0    # hoạt động gọn, dễ sắp xếp
        elif time_ratio <= 0.8:
            time_score = 1.0 - (time_ratio - 0.5) / 0.3
        else:
            time_score = max(0.0, 1.0 - time_ratio)
    else:
        time_score = 0.5

    if time_score >= 0.7:
        reasons.append(f"Thời gian vừa phải ({act['time']} phút)")

    # ---------- 5. Diversity Bonus (0 – 1) ----------
    tag_key = frozenset(act_tag_set)
    if tag_key not in seen_tag_groups:
        diversity = 1.0
        reasons.append("Đa dạng hóa trải nghiệm")
    else:
        diversity = 0.3

    # ---------- Tổng hợp (gồm 5 nhân tố từ 1-5) ----------
    weights = SCORING_WEIGHTS
    weighted_sum = (
        weights["tag_overlap"]      * tag_overlap
        + weights["location_synergy"] * location_synergy
        + weights["cost_efficiency"]  * cost_score
        + weights["time_fit"]         * time_score
        + weights["diversity_bonus"]  * diversity
    )

    # ---------- 6. Nhân với Location Score từ N4 ----------
    # location_score từ N4 (ranking score): phản ánh mức độ phù hợp từ bước N4
    # Nhân vào để điểm cuối được hiệu chỉnh theo ranking từ N4
    # Ví dụ: location có score 0.85 từ N4 sẽ làm tăng activities tổng thể 15%
    final = round(weighted_sum * location_score, 2)

    # Nếu không có reason nào → activity quá chung chung
    if not reasons:
        reasons.append("Hoạt động phổ biến tại địa điểm này")

    return final, reasons


def generate_activities(
    user_tags: List[str],
    locations: List[Dict],
    constraints: Dict[str, Any] = None
) -> List[Dict]:
    """
    N5 - Activity Generation (Improved)

    Cải tiến:
      • match_score tính theo 5 chiều: tag overlap, location synergy,
        cost efficiency, time fit, diversity bonus.
      • Constraints lọc chặt: budget/activity, time/activity, exclude_tags,
        min_match_score.
      • Trả về danh sách reasons chi tiết cho từng hoạt động.
    """
    cons = _merge_constraints(constraints)
    result: List[Dict] = []
    seen_tag_groups: set = set()                # để tính diversity bonus
    rejected_log: List[Dict] = []               # log các activity bị loại (debug)

    for loc in locations:
        loc_name = loc.get("name")
        if loc_name not in ACTIVITY_TEMPLATES:
            continue

        template = ACTIVITY_TEMPLATES[loc_name]
        location_tags = template.get("tags", [])
        activities = template["activities"]

        for act in activities:
            # ---- Bước 1: Kiểm tra constraints ----
            passed, reject_reason = _passes_constraints(act, cons)
            if not passed:
                rejected_log.append({
                    "name": act["name"],
                    "location": loc_name,
                    "reason": reject_reason,
                })
                continue

            # ---- Bước 2: Tính match_score ----
            score, reasons = _compute_match_score(
                act, user_tags, location_tags, cons, seen_tag_groups
            )

            # ---- Bước 3: Lọc theo min_match_score ----
            if score < cons["min_match_score"]:
                rejected_log.append({
                    "name": act["name"],
                    "location": loc_name,
                    "reason": f"match_score {score} < ngưỡng {cons['min_match_score']}",
                })
                continue

            # Cập nhật seen groups cho diversity
            seen_tag_groups.add(frozenset(act["tags"]))

            # ---- Bước 4: Tạo output ----
            activity = {
                "activity_id": f"{loc_name.lower().replace(' ', '_')}_{act['name'].lower().replace(' ', '_')}",
                "location_id": loc_name,
                "location_name": loc_name,
                "name": act["name"],
                "description": act["desc"],
                "cost": act["cost"],
                "estimated_time_minutes": act["time"],
                "tags": act["tags"],
                "match_score": score,
                "reasons": reasons,
                "reason_summary": " · ".join(reasons),
                "generated_by": "template",    # Đánh dấu nguồn: rule-based template
            }
            result.append(activity)

    # ---- Sắp xếp theo match_score giảm dần, tie-break theo cost tăng dần ----
    result.sort(key=lambda x: (-x["match_score"], x["cost"]))

    max_activities = cons.get("max_activities", 12)
    final = result[:max_activities]

    return final


# =============================================================================
# HYBRID APPROACH: KẾT HỢP LLM + RULE-BASED
# =============================================================================
# Tại sao chọn Hybrid?
#   1. Rule-based (template) đảm bảo tính ổn định: luôn có kết quả, không phụ
#      thuộc mạng hay API bên ngoài. Tuy nhiên, dữ liệu bị giới hạn bởi
#      số lượng template đã xây dựng thủ công.
#   2. LLM (Gemini) mang lại tính linh hoạt: có thể sinh hoạt động cho bất kỳ
#      địa điểm nào, cá nhân hóa theo context cụ thể của user. Tuy nhiên,
#      phụ thuộc vào API key và kết nối mạng.
#   3. Hybrid kết hợp ưu điểm cả hai: ưu tiên dùng LLM khi có thể, fallback
#      về template khi LLM không khả dụng. Kết quả từ LLM vẫn phải qua
#      pipeline post-processing giống template (constraint checking, scoring)
#      để đảm bảo chất lượng đồng nhất.
# =============================================================================


def _post_process_llm_activities(
    llm_activities: List[Dict],
    location_name: str,
    user_tags: List[str],
    location_tags: List[str],
    constraints: Dict[str, Any],
    seen_tag_groups: set,
) -> List[Dict]:
    """
    Post-processing cho activities sinh từ LLM.
    
    Áp dụng cùng pipeline xử lý như rule-based:
      1. Kiểm tra constraints (budget, time, exclude_tags)
      2. Tính match_score theo 5 chiều
      3. Thêm trường "reason" và "generated_by": "llm"
    
    Đảm bảo output từ LLM có cùng format và chất lượng như template.
    """
    result = []
    
    for act in llm_activities:
        # ---- Bước 1: Kiểm tra constraints ----
        passed, reject_reason = _passes_constraints(act, constraints)
        if not passed:
            logger.debug(f"LLM activity bị loại: {act['name']} - {reject_reason}")
            continue
        
        # ---- Bước 2: Tính match_score ----
        score, reasons = _compute_match_score(
            act, user_tags, location_tags, constraints, seen_tag_groups
        )
        
        # ---- Bước 3: Lọc theo min_match_score ----
        if score < constraints.get("min_match_score", 0.1):
            logger.debug(f"LLM activity score quá thấp: {act['name']} ({score})")
            continue
        
        # Cập nhật seen groups cho diversity
        seen_tag_groups.add(frozenset(act["tags"]))
        
        # ---- Bước 4: Tạo output với đánh dấu generated_by ----
        activity = {
            "activity_id": f"{location_name.lower().replace(' ', '_')}_{act['name'].lower().replace(' ', '_')}",
            "location_id": location_name,
            "location_name": location_name,
            "name": act["name"],
            "description": act["desc"],
            "cost": act["cost"],
            "estimated_time_minutes": act["time"],
            "tags": act["tags"],
            "match_score": score,
            "reasons": reasons,
            "reason_summary": " · ".join(reasons),
            "generated_by": "llm",    # Đánh dấu nguồn: sinh bởi LLM
        }
        result.append(activity)
    
    return result


def generate_activities_hybrid(
    user_tags: List[str],
    locations: List[Dict],
    constraints: Dict[str, Any] = None,
    use_llm: bool = True,
) -> List[Dict]:
    """
    N5 - Hybrid Activity Generation (LLM + Rule-based).
    
    Chiến lược hybrid:
      - Nếu use_llm=True VÀ có API key → thử dùng LLM (Gemini) trước.
        + LLM thành công → dùng kết quả LLM, qua post-processing.
        + LLM thất bại → fallback về rule-based template.
      - Nếu use_llm=False HOẶC không có API key → dùng rule-based thuần túy.
    
    Kết quả từ cả 2 nguồn đều qua cùng pipeline:
      constraint checking → match_score → sorting → limit.
    
    Args:
        user_tags: Danh sách sở thích của người dùng (VD: ["nature", "food"])
        locations: Danh sách địa điểm (VD: [{"name": "Sa Pa", "description": "..."}])
        constraints: Ràng buộc ngân sách, thời gian, v.v.
        use_llm: True để thử dùng LLM, False để chỉ dùng rule-based.
    
    Returns:
        Danh sách activities đã sắp xếp theo match_score, mỗi activity có
        trường "generated_by" cho biết nguồn sinh ("llm" hoặc "template").
    """
    cons = _merge_constraints(constraints)
    result: List[Dict] = []
    seen_tag_groups: set = set()
    
    # Xác định xem có thể dùng LLM hay không
    can_use_llm = (
        use_llm
        and LLM_MODULE_AVAILABLE
        and _is_llm_available()
    )
    
    if can_use_llm:
        logger.info("Hybrid mode: Sử dụng LLM (Gemini) để sinh hoạt động")
    else:
        if use_llm and not LLM_MODULE_AVAILABLE:
            logger.info("LLM module không khả dụng, fallback về rule-based")
        elif use_llm and not _is_llm_available():
            logger.info("Không có GEMINI_API_KEY, fallback về rule-based")
        else:
            logger.info("Rule-based mode: Chỉ dùng template")
    
    for loc in locations:
        loc_name = loc.get("name")
        loc_desc = loc.get("description", f"Địa điểm du lịch {loc_name} tại Việt Nam")
        
        llm_success = False
        
        # ===== THỬ LLM TRƯỚC (nếu được bật) =====
        if can_use_llm:
            try:
                llm_activities = generate_activities_from_llm(
                    location_name=loc_name,
                    location_description=loc_desc,
                    user_tags=user_tags,
                    budget=int(cons["max_cost_per_activity"]),
                    max_time_per_activity=int(cons["max_time_per_activity"]),
                )
                
                if llm_activities:
                    # Post-processing: lọc constraints, tính score, thêm metadata
                    location_tags = []
                    # Lấy location tags từ template nếu có (để tính location_synergy)
                    if loc_name in ACTIVITY_TEMPLATES:
                        location_tags = ACTIVITY_TEMPLATES[loc_name].get("tags", [])
                    
                    processed = _post_process_llm_activities(
                        llm_activities=llm_activities,
                        location_name=loc_name,
                        user_tags=user_tags,
                        location_tags=location_tags,
                        constraints=cons,
                        seen_tag_groups=seen_tag_groups,
                    )
                    
                    if processed:
                        result.extend(processed)
                        llm_success = True
                        logger.info(
                            f"LLM sinh thành công {len(processed)} hoạt động "
                            f"cho {loc_name} (sau post-processing)"
                        )
                    
            except Exception as e:
                logger.warning(f"LLM thất bại cho {loc_name}: {e}, fallback template")
        
        # ===== FALLBACK VỀ RULE-BASED NẾU LLM KHÔNG THÀNH CÔNG =====
        if not llm_success:
            if loc_name not in ACTIVITY_TEMPLATES:
                logger.debug(f"Không có template cho {loc_name}, bỏ qua")
                continue
            
            template = ACTIVITY_TEMPLATES[loc_name]
            location_tags = template.get("tags", [])
            activities = template["activities"]
            
            for act in activities:
                # Kiểm tra constraints
                passed, reject_reason = _passes_constraints(act, cons)
                if not passed:
                    continue
                
                # Tính match_score
                score, reasons = _compute_match_score(
                    act, user_tags, location_tags, cons, seen_tag_groups
                )
                
                # Lọc theo min_match_score
                if score < cons["min_match_score"]:
                    continue
                
                # Cập nhật diversity tracker
                seen_tag_groups.add(frozenset(act["tags"]))
                
                # Tạo output
                activity = {
                    "activity_id": f"{loc_name.lower().replace(' ', '_')}_{act['name'].lower().replace(' ', '_')}",
                    "location_id": loc_name,
                    "location_name": loc_name,
                    "name": act["name"],
                    "description": act["desc"],
                    "cost": act["cost"],
                    "estimated_time_minutes": act["time"],
                    "tags": act["tags"],
                    "match_score": score,
                    "reasons": reasons,
                    "reason_summary": " · ".join(reasons),
                    "generated_by": "template",    # Fallback: dùng template
                }
                result.append(activity)
    
    # ---- Sắp xếp theo match_score giảm dần, tie-break theo cost tăng dần ----
    result.sort(key=lambda x: (-x["match_score"], x["cost"]))
    
    max_activities = cons.get("max_activities", 12)
    final = result[:max_activities]
    
    # Log thống kê nguồn
    llm_count = sum(1 for a in final if a.get("generated_by") == "llm")
    template_count = sum(1 for a in final if a.get("generated_by") == "template")
    logger.info(f"Kết quả hybrid: {llm_count} LLM + {template_count} template = {len(final)} tổng")
    
    return final


# ====================== TEST CASES ======================
if __name__ == "__main__":
    import textwrap

    def _print_results(title: str, activities: List[Dict]):
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}")
        for i, a in enumerate(activities, 1):
            print(f"\n  [{i}] {a['name']}  ({a['location_name']})")
            print(f"      Score: {a['match_score']}  |  Cost: {a['cost']:,}đ  |  Time: {a['estimated_time_minutes']} phút")
            print(f"      Tags: {', '.join(a['tags'])}")
            print(f"      Reasons: {a['reason_summary']}")
        if not activities:
            print("  (Không có hoạt động nào phù hợp)")
        print()

    # ---- Test 1: User thích thiên nhiên + phiêu lưu ----
    _print_results(
        "Test 1: nature + adventure + trekking",
        generate_activities(
            user_tags=["nature", "adventure", "trekking"],
            locations=[{"name": "Sa Pa"}, {"name": "Đà Lạt"}, {"name": "Phú Quốc"}],
            constraints={"budget": 5_000_000, "max_time_per_day": 480},
        ),
    )

    # ---- Test 2: User thích ẩm thực + văn hóa, ngân sách thấp ----
    _print_results(
        "Test 2: food + culture, budget 2M",
        generate_activities(
            user_tags=["food", "culture"],
            locations=[{"name": "Sa Pa"}, {"name": "Đà Lạt"}],
            constraints={"budget": 2_000_000, "max_time_per_day": 360},
        ),
    )

    # ---- Test 3: Loại bỏ adventure ----
    _print_results(
        "Test 3: nature, exclude_tags=['adventure']",
        generate_activities(
            user_tags=["nature", "relax"],
            locations=[{"name": "Sa Pa"}, {"name": "Phú Quốc"}],
            constraints={
                "budget": 5_000_000,
                "exclude_tags": ["adventure"],
            },
        ),
    )

    # ---- Test 4: JSON đầy đủ ----
    print("\n=== JSON Output (Test 1) ===")
    activities = generate_activities(
        user_tags=["nature", "adventure", "trekking"],
        locations=[{"name": "Sa Pa"}, {"name": "Đà Lạt"}, {"name": "Phú Quốc"}],
        constraints={"budget": 5_000_000},
    )
    print(json.dumps(activities, indent=2, ensure_ascii=False))