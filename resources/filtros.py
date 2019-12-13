def normalize_path_params(city=None, 
                            rating_min=0, 
                            rating_max=5, 
                            dailyvalue_min=0, 
                            dailyvalue_max=10000,
                            limit=50, offset=0, **dados):
    if city:
        return {
            'rating_min': rating_min,
            'rating_max': rating_max,
            'dailyvalue_min': dailyvalue_min,
            'dailyvalue_max': dailyvalue_max,
            'city': city,
            'limit': limit,
            'offset': offset
        }
    return {
            'rating_min': rating_min,
            'rating_max': rating_max,
            'dailyvalue_min': dailyvalue_min,
            'dailyvalue_max': dailyvalue_max,
            'limit': limit,
            'offset': offset
            }
query_without_city = "SELECT * FROM hoteis \
            WHERE (rating >= ? and rating <= ?) \
                and (dailyvalue >= ? and dailyvalue <= ?) \
                    LIMIT ? OFFSET ?"

query_with_city = "SELECT * FROM hoteis \
            WHERE (rating >= ? and rating <= ?) \
                and (dailyvalue >= ? and dailyvalue <= ?) \
                    and (city = ?) \
                    LIMIT ? OFFSET ?"