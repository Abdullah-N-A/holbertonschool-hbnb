from flask_restx import Namespace, Resource, fields
from app.business.models.facade import HBnBFacade
from app.models.review import Review
from app.models.user import User
from app.models.place import Place

facade = HBnBFacade()

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5'),
    'user_id': fields.String(required=True, description='ID of the user who writes the review'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed')
})
@api.route('/')
class ReviewList(Resource):
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        reviews = [obj for obj in facade.get_all() if isinstance(obj, Review)]
        result = []
        for r in reviews:
            result.append({
                'id': r.id,
                'text': r.text,
                'rating': r.rating,
                'user_id': r.user.id,
                'place_id': r.place.id,
                'created_at': r.created_at.isoformat(),
                'updated_at': r.updated_at.isoformat()
            })
        return result, 200

    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review"""
        data = api.payload or {}

        # Validate required fields
        required_fields = ['text', 'rating', 'user_id', 'place_id']
        for field in required_fields:
            if field not in data:
                return {'error': f'{field} is required'}, 400

        # Validate user
        user = facade.get(data['user_id'])
        if not user or not isinstance(user, User):
            return {'error': 'User not found'}, 400

        # Validate place
        place = facade.get(data['place_id'])
        if not place or not isinstance(place, Place):
            return {'error': 'Place not found'}, 400

        # Create review
        new_review = Review(
            text=data['text'],
            rating=data['rating'],
            user=user,
            place=place
        )

        created_review = facade.create(new_review)

        return {
            'id': created_review.id,
            'text': created_review.text,
            'rating': created_review.rating,
            'user_id': created_review.user.id,
            'place_id': created_review.place.id,
            'created_at': created_review.created_at.isoformat(),
            'updated_at': created_review.updated_at.isoformat()
        }, 201


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review by ID"""
        r = facade.get(review_id)
        if not r or not isinstance(r, Review):
            return {'error': 'Review not found'}, 404

        return {
            'id': r.id,
            'text': r.text,
            'rating': r.rating,
            'user_id': r.user.id,
            'place_id': r.place.id,
            'created_at': r.created_at.isoformat(),
            'updated_at': r.updated_at.isoformat()
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update review"""
        r = facade.get(review_id)
        if not r or not isinstance(r, Review):
            return {'error': 'Review not found'}, 404

        data = api.payload or {}
        updated_review = facade.update(review_id, data)

        return {
            'id': updated_review.id,
            'text': updated_review.text,
            'rating': updated_review.rating,
            'user_id': updated_review.user.id,
            'place_id': updated_review.place.id,
            'created_at': updated_review.created_at.isoformat(),
            'updated_at': updated_review.updated_at.isoformat()
        }, 200

    @api.response(204, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete review"""
        r = facade.get(review_id)
        if not r or not isinstance(r, Review):
            return {'error': 'Review not found'}, 404

        facade.delete(review_id)
        return '', 204
