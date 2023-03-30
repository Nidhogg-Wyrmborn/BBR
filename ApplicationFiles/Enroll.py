import ctypes
from ctypes import wintypes

SECURITY_MAX_SID_SIZE = 68
WINBIO_TYPE_FINGERPRINT = 0x00000008
WINBIO_POOL_SYSTEM = 0x00000001
WINBIO_FLAG_DEFAULT = 0x00000000
WINBIO_ID_TYPE_SID = 3

# Error Info
WINBIO_E_NO_MATCH = 0x80098005

isNewTemplate = True
session_handle = ctypes.c_uint32()
unit_id = ctypes.c_uint32()
subFactor = ctypes.c_ubyte(0xf5)
reject_detail = ctypes.c_uint32()

class GUID(ctypes.Structure):
	_fields_ = [("Data1", wintypes.DWORD),
				("Data2", wintypes.WORD),
				("Data3", wintypes.WORD),
				("Data4", wintypes.BYTE * 8)
				]

class AccountSid(ctypes.Structure):
	_fields_ = [("Size", wintypes.ULONG),
				("Data", ctypes.c_ubyte * SECURITY_MAX_SID_SIZE)
				]

class Value(ctypes.Union):
	_fields_ = [("NULL", wintypes.ULONG),
				("Wildcard", wintypes.ULONG),
				("TemplateGuid", GUID),
				("AccountSid", AccountSid)
				]

class WINBIO_IDENTITY(ctypes.Structure):
	_fields_ = [("Type", ctypes.c_uint32),
			("Value", Value)]

identity = WINBIO_IDENTITY()

lib = ctypes.WinDLL(r"C:\Windows\System32\winbio.dll")

def close():
	if session_handle != None:
		lib.WinBioCloseSession(session_handle)
		session_handle = None
	input("Press enter to continue")
	quit()

try:
	hr = lib.WinBioOpenSession(
		WINBIO_TYPE_FINGERPRINT,
		WINBIO_POOL_SYSTEM,
		WINBIO_FLAG_DEFAULT,
		None,
		0,
		None,
		ctypes.byref(session_handle))
	if hr & 0xffffffff != 0x0:
			print("Open Failed!")
			quit()
except Exception as e:
	print("Open Failed\n")
	print(e)
	close()

try:
	sensor = lib.WinBioLocateSensor(session_handle, ctypes.byref(unit_id))
	if sensor & 0xffffffff != 0x0:
		print("Local Failed!")
		yut090quit()
except Exception as e:
	print("Locate Failed!\n")
	print(e)
	close()

print('starting enrollment sequence')
try:
	enroll = lib.WinBioEnrollBegin(
		session_handle,
		subFactor,
		unit_id)
except Exception as e:
	print("Error\n")
	print(e)
	close()

s = 1
swipecount = 1
running = True
while running:
	try:
		print(f"Swipe the sensor to capture {s} sample", end='')
		if swipecount == 1:
			statement = "The first"
		elif swipecount > 1:
			statement = "another"
		else:
			statement = 'asdf'
		print(statement)
		cap = lib.WinBioEnrollCapture(
			session_handle,
			reject_detail)
		print(f"Sample {s} captured from sensor "+str(swipecount)+" "+str(unit_id))
		swipecount += 1
		s += 1
		if cap == WINBIO_I_MORE_DATA:
			print("More data required")
			continue
		else:
			print("Template completed.\n")
			break
	except Exception as e:
		try:
			if cap == lib.WINBIO_E_BAD_CAPTURE:
				print(f"Error: bad capture; reason; {reject_detail}")
				continue
			else:
				print("WinBioEnrollCapture failed. cap = {cap}")
				print(e)
				close()
		except:
			print("Error, capture failed")
			print(e)
if discardEnrollment == True:
	try:
		print("Discarding enrollment...\n\n")
		discard = lib.WinBioEnrollDiscard(session_handle)
	except Exception as e:
		print(f"WinBioLocateSensor failed. discard = {discard}")
		print(e)
		close()
else:
	try:
		print("Committing enrollment...\n")
		commit = lib.WinBioEnrollCommit(
			session_handle,
			identity,
			isNewTemplate)
	except Exception as e:
		print(f"WinBioEnrollCommit failed. commit = {commit}")
		print(e)
		close()
