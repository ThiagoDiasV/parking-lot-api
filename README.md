# Parking MK Rest API

Parking MK is a Rest API for parking lots.

## How to Install

[Refer to this link](https://github.com/ThiagoDiasV/parking-mk-challenge/blob/master/INSTALL.md) of INSTALL.md to proceed with installation.

# Rest API

## Endpoints

    /parking/
    /parking/{id}/
    /parking/{plate}/
    /parking/{id}/pay/
    /parking/{id}/out/

## Examples

### List entire data

Returns json or html with entire data

- URL

  /parking/

- Method

  GET

- URL params

  None

- Data params

  None

- Success Response

  - HTTP status code

    200 OK

  - Content

    [{"id":1,"entry_time":"2020-01-12T19:23:45.872121-03:00","left_time":"2020-01-12T19:24:40.118585-03:00","time":"1 minutes","paid":true,"left":true,"plate":"AAA-9999"},{"id":2,"entry_time":"2020-01-12T19:23:54.474840-03:00","left_time":"2019-12-31T21:00:00-03:00","time":"0 minutes","paid":false,"left":false,"plate":"AAA-1234"},{"id":3,"entry_time":"2020-01-12T19:23:59.550934-03:00","left_time":"2020-01-12T19:24:12.703355-03:00","time":"0 minutes","paid":true,"left":false,"plate":"ABC-1234"},{"id":4,"entry_time":"2020-01-12T19:24:09.177472-03:00","left_time":"2019-12-31T21:00:00-03:00","time":"0 minutes","paid":false,"left":false,"plate":"AZA-5511"}]

### Create new car instance register

Returns json or html data with created entry.

- URL

  /parking/

- Method

  POST

- URL params

  None

- Data params

  Required:

        plate=[string]

- Success Response

  - HTTP status code

    201 CREATED

  - Content

    {
    "id": 5,
    "entry_time": "2020-01-12T19:28:22.009154-03:00",
    "left_time": "2020-01-01T00:00:00.000000Z",
    "time": "0 minutes",
    "paid": false,
    "left": false,
    "plate": "OBA-1234"
    }

- Error Response

  - HTTP status code

    400 BAD REQUEST

  - Content

    {
    "plate": [
    "OBA-12345 isn't a valid plate format. The correct format is AAA-1111",
    "Ensure this field has no more than 8 characters."
    ]
    }
