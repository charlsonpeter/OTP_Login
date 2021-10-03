Steps
=====

1) Migrate project by run "python manage.py makemigrations" and "python manage.py migrate"
2) Please run the project (python manage.py runserver)


1) Get OTP:
  URL: 	http://localhost:8000/get_otp/
	Method:  POST
	Payload: {"mob_no":xxxxxxxxxx}

2) Verify OTP:
  URL: 	http://localhost:8000/verify_otp/
	Method:  POST
	Payload: {"mob_no":xxxxxxxxxx, "otp":xxxxxx}
