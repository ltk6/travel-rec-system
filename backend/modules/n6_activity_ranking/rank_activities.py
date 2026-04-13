import numpy as np

def rank_activities(vector, activities, constraints, top_k):
    """
    N6 - Activity Ranking
    Xếp hạng các hoạt động dựa trên độ tương đồng với sở thích người dùng (vector)
    """
    if not activities or top_k <= 0:
        return {"activities":[]}
    # chuyển vector người dùng sang numpy array
    user_vec=np.array(vector, dtype=float)
    user_norm=np.linalg.norm(user_vec)

    #lấy ràng buộc nếu người dùng không đề cập tới các biến cố định sau
    max_cost=constraints.get("max_cost",10**9)       # mặc định số tiền nhiều nhất cho chuyến đi là 10^9
    max_time=constraints.get("max_time",10**9)       #mặc định thời gian cho chuyến đi là 10^9 giờ
    min_rating=constraints.get("min_rating",0.0)      #mặc định số sao đánh giá của activitive là 0

    scored_list=[]
    for act in activities:
        #lấy vè kiểm tra vector hoạt động
        raw_act_vec=act.get("embedding") or act.get("vector")
        if raw_act_vec is None:
            continue

        act_vec=np.array(raw_act_vec, dtype=float)
        # lọc nhanh theo ràng buộc cứng (cost, time , rating), lấy thông tin cơ bản
        cost=float(act.get("cost",0))
        time=float(act.get("time",0))
        rating=float(act.get("rating",0))

        if cost > max_cost or time > max_time or rating < min_rating:
            continue
        # tính cos(0) similarity bằng Numpy
        act_norm=np.linalg.norm(act_vec)
        similarity=0.0
        if user_norm > 0 and act_norm > 0:
            # tính độ tương đồng cos(0): dot(a, b) / (||a|| * ||b||)
            # kết quả gần 1: rất khớp sở thích | Gần 0: không liên quan
            similarity=np.dot(user_vec, act_vec)/(user_norm * act_norm)
        # tính điểm thành phần Normalize về thang 0-1
        rating_score = rating / 5.0 if rating > 0 else 0.0

        #tránh lỗi chia cho 0 nếu max_cost và max time được set về 0
        cost_penalty = (cost / max_cost) if max_cost > 0 else 0
        time_penalty = (time / max_time) if max_time > 0 else 0
        
        # mặc định cho chương trình với công thức tính điểm tổng
        # với final score : 65% similarity, 20% rating, -10% cost, -5% time
        final_score = (0.65*similarity) + (0.20 * rating_score) - (0.10 * cost_penalty) - (0.05 * time_penalty)

        #thêm vào danh sách
        scored_list.append({
            "activity_id":act.get("activity_id"),
            "location_id":act.get("location_id"),
            "score":round(float(final_score),4),
            "cost":cost,
            "time":time,
            #"similarity":round(float(similarity),4) trả về để debug nếu cần
        })
    #sắp xếp lại và lấy top K theo yêu cầu người dùng  
    scored_list.sort(key=lambda x: x["score"], reverse=True)

    return {"activities": scored_list[:top_k]}