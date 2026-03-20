import itertools

class CandidateGenerator:
    def __init__(self, user_hist, item_data, pop_items):
        # basic dictionaries for dummy data
        self.users = user_hist
        self.items = item_data
        self.popular = pop_items

    def collaborative_candidates(self, uid, limit=20):
        def gen_collab():
            if uid not in self.users: return
            my_items = set(self.users[uid])
            
            for other_u, their_items in self.users.items():
                if other_u == uid: continue
                # if we share at least 1 item
                if my_items & set(their_items):
                    for item in their_items:
                        if item not in my_items:
                            yield item
        
        # filter out duplicates on the fly
        seen = set()
        res = []
        for i in gen_collab():
            if i not in seen:
                seen.add(i)
                res.append(i)
                if len(res) >= limit: break
        return res

    def content_based_candidates(self, uid, limit=20):
        def gen_content():
            if uid not in self.users: return
            my_items = self.users[uid]
            
            # get all tags user has interacted with
            my_tags = set()
            for i in my_items:
                my_tags.update(self.items.get(i, []))
            
            for item, tags in self.items.items():
                if item not in my_items and (my_tags & set(tags)):
                    yield item
        
        return list(itertools.islice(gen_content(), limit))

    def popularity_candidates(self, limit=20):
        return self.popular[:limit]

    def hybrid_candidates(self, uid, limit=30):
        # handle cold start for brand new users
        if uid not in self.users or not self.users[uid]:
            return self.popularity_candidates(limit)
        
        collab = self.collaborative_candidates(uid, limit//2)
        content = self.content_based_candidates(uid, limit//2)
        
        combined = list(set(collab + content))
        
        # pad with popular items if we dont have enough
        if len(combined) < limit:
            for p in self.popularity_candidates(limit):
                if p not in combined:
                    combined.append(p)
                    if len(combined) >= limit: break
                    
        return combined[:limit]