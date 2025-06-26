from rest_framework.throttling import UserRateThrottle

class BookThrottle(UserRateThrottle):
    scope = 'book-throttle'

class BorrowThrottle(UserRateThrottle):
    scope = 'borrow-throttle'
