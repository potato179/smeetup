

profile_model = user.model(
    "Profile", {
        "username": fields.String(description='사용자 이름(ID)', required=True, example="1234")
    }
)

review_model = review.model(
    "Review", {

    }
)
