1. Resource :Users, profies, posts, tags,comments,following, followers.
2. Phân loại collection/item/sub-resource<br>
    collection:posts, users, tags <br>
    item: /posts/{post_id}, /users/{user_id}, /tags/{tag_id}<br>
    sub-resource:/posts/{post_id}/comments, users/{user_id}/followers <br>
3. tree endpoint
![](<tree endpoint.jpg>)
version segment: v1. ex: /api/v1/users/post?user_id=[id]
4.