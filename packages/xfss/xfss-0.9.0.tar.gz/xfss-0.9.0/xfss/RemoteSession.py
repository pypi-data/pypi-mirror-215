from functools import update_wrapper

import requests
import validators
from flask import request, Response

from xfss.HTTPStatus import HTTPStatus, NOT_ACCEPTABLE


class RemoteSession:
	"""
	A helper class to handle sessions in remote XF type servers.


	Be sure to set te target address before any operation:

	>>> RemoteSession.set_address("192.168.1.100")

	Set a target port like this:

	>>> RemoteSession.set_port("100")

	To create a new remote session, provide the required values and shoot:

	>>> payload = {"email": "mail@mail.com", "password": "g00dP4ss0rD"}
	>>> response = RemoteSession.init_session(payload)

	>>> http_status = response[0]
	>>> if http_status == 201:
	>>> 	session_token = response[1]

	Store the provided token in a safe place. You will need it for future requests.

	Documentation still on the works.
	If you need any help, do not think twice about writing a mail to:

	edsonmanuelcarballovera@gmail.com

	or look for me on Twitter at:

	@EdsonManuelVera

	Shoutout to Kenneth Reitz for providing an easy way to do RESTful calls.

	:copyright: (c) 2022 by Edson Manuel Carballo Vera.
	:license: MIT.
	"""
	session_server_address: str or None = None
	session_server_port: str or int or None = None

	@staticmethod
	def __get_full_url() -> str:
		if RemoteSession.session_server_address is not None:
			url: str = RemoteSession.session_server_address
			if RemoteSession.session_server_port is not None:
				url += ":" + str(RemoteSession.session_server_port)
			return url
		else:
			raise TypeError("Session Server address is not set. Set it with RemoteSession.set_address")

	@staticmethod
	def set_address(address: str) -> None:
		r"""Sets the address of the remote session server

		:param address: The target address
		:raises ValueError: If the address is not a valid URL, IPV4 or IPV6 address.
		:raises TypeError: If the address is not a string
		"""
		if address is not None:
			if validators.url(address) or validators.ipv4(address) or validators.ipv6(address):
				RemoteSession.session_server_address = address
			else:
				raise ValueError("Address is not valid")
		else:
			raise TypeError("Address is not valid")

	@staticmethod
	def set_port(port: str or int) -> None:
		r"""Sets the port of the remote session server

		:param port: The target port
		:raises ValueError: If the port is not between 1 and 65,535
		:raises TypeError: If the port is and string or an integer
		"""
		if port is not None:
			if 1 <= port <= 65_535:
				RemoteSession.session_server_port = port
			else:
				raise ValueError("Port number is not a valid port")
		else:
			raise TypeError("Port is not valid")

	@staticmethod
	def init_session(payload: dict) -> dict:
		r"""Creates a new session on the remote session server.

		:param payload: Dictionary with the email, password and role (optional) of the user to log in.
		:return: A tuple with an HTTP status code and the session token if successful. HTTP Status code and None if not.
		:raises ValueError: If the required values are not set.
		:raises TypeError: If the remote server address is not set.
		"""
		if "email" in payload and "password" in payload:
			if "role" not in payload:
				payload["role"] = None

			url: str = RemoteSession.__get_full_url()
			url += "/session"

			response = requests.post(url, json=payload)
			if response.status_code == HTTPStatus.RESOURCE_CREATED.value:
				return {
					"STATUS": response.status_code,
					"TOKEN": response.json()["token"]
				}
			return {"STATUS": response.status_code, "TOKEN": None}
		else:
			raise ValueError("Email and password are required")

	@staticmethod
	def get_session_info(token: str) -> dict or int:
		r"""Get the information stored on the server.

		This does not destroy or affect the session.

		:param token: The session token provided when the session was started.
		:return: A dictionary with the information stored on the remote server.
			An int with the HTTP status code if anything fails.
		:raises TypeError: If the token is not valid or None.
		"""
		if token is not None:
			url: str = RemoteSession.__get_full_url()
			url += "/session"

			headers: dict = {"token": token}

			response = requests.get(url, headers=headers)
			if response.status_code == HTTPStatus.OK.value:
				return response.json()
			else:
				return response.status_code
		else:
			raise TypeError("Token is not valid")

	@staticmethod
	def update_session(token: str, new_data: dict) -> dict or int:
		r"""Updates the session information

		THIS ACTION IS DESTRUCTIVE. THE NEW INFORMATION WILL OVERRIDE ALL INFORMATION ON THE SESSION.
		It's recommended that you retrieve the stored information and then append the new information to that.
		Otherwise, the old information will be lost.
		:param token: The session token provided when the session was started.
		:param new_data: The new data that will be stored on the server.
		:return: A dict with all the information on the session after the update is performed.
		An int with the status code if the request fails.
		:raises TypeError: If the token is not valid or None.
		"""
		if token is not None and new_data is not None:
			url: str = RemoteSession.__get_full_url()
			url += "/session"

			headers: dict = {"token": token}

			response = requests.patch(url, json=new_data, headers=headers)
			if response.status_code == HTTPStatus.OK.value:
				return response.json()
			else:
				return response.status_code
		else:
			raise TypeError("Token or new data is not valid")

	@staticmethod
	def is_session_alive(token: str) -> bool:
		r"""Check if the session is still alive in the remote server

		:param token: The session token provided when the session was started.
		:return: A boolean indicating if the session is alive.
		:raises TypeError: If the token is not valid or None.
		"""
		if token is not None:
			url: str = RemoteSession.__get_full_url()
			url += "/session"

			headers: dict = {"token": token}

			response = requests.put(url, headers=headers)
			return response.status_code == HTTPStatus.OK.value
		else:
			raise TypeError("Token is not valid")

	@staticmethod
	def close_session(token: str) -> bool:
		r"""Closes the session in the remote server.

		THIS ACTION IS DESTRUCTIVE AND CANNOT BE REVERTED.

		:param token: The session token provided when the session was started.
		:returns: A boolean indicating if the session was closed successfully or not.
		Any way, after this action, the session should be considered lost.
		:raises TypeError: If the token is not valid or None.
		"""
		if token is not None:
			url: str = RemoteSession.__get_full_url()
			url += "/session"

			headers: dict = {"token": token}

			response = requests.delete(url, headers=headers)
			return response.status_code == HTTPStatus.OK.value
		else:
			raise TypeError("Token is not valid")

	@staticmethod
	def requires_token(operation):
		r""" Use this oneliner decorator to indicate that a route operation requires a token to be processed.

		If the token is not present, adequate responses will be sent according to the case.
		"""

		def verify_auth(*args, **kwargs):
			token = request.headers.get("token")
			if token is not None:
				url: str = RemoteSession.__get_full_url()
				url += "/requires_token"

				headers: dict = {"token": token}

				request_result = requests.get(url, headers=headers)
				if request_result.status_code == HTTPStatus.OK.value:
					response = operation(*args, **kwargs)
				else:
					response = Response(status=request_result.status_code)
			else:
				response = Response(status=NOT_ACCEPTABLE)
			return response

		return update_wrapper(verify_auth, operation)

	@staticmethod
	def requires_role(role: str or list):
		r"""Use this oneliner decorator to indicate that a route operation requires a specific user role to be processed.
		If you use this, there is no need to use StatefulSession.requires_token.
		If the token is not present, or the user role does not match, adequate responses will be sent according to the case.
		"""

		def decorator(operation):
			def verify_role(*args, **kwargs):
				token = request.headers.get("token")
				if token is not None:
					url: str = RemoteSession.__get_full_url() + "/requires_role"

					headers: dict = {"token": token}
					payload: dict = {"role": role}

					request_result = requests.get(url, headers=headers, json=payload)
					if request_result.status_code == HTTPStatus.OK.value:
						response = operation(*args, **kwargs)
					else:
						response = Response(status=request_result.status_code)
				else:
					response = Response(status=NOT_ACCEPTABLE)
				return response

			return update_wrapper(verify_role, operation)

		return decorator
