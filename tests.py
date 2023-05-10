from handler import calendar_generator



def test_invalid_year():
    event = {
        'pathParameters': {
            'year': 'randomString'
        }
    }
    context = {}
    response = calendar_generator(event, context)
    assert response['statusCode'] == 400
    assert f"Error in year format: {event['pathParameters'].get('year', 'Unknown')}" in response['body']


def test_valid_year():
    event = {
        'pathParameters': {
            'year': '2021'
        }
    }
    context = {}
    response = calendar_generator(event, context)
    assert response['statusCode'] == 200
    assert response['headers']['Content-Type'] == 'application/json' 