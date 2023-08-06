import usb.core
import usb.backend.libusb1
import libusb_package


_backend = usb.backend.libusb1.get_backend(find_library=libusb_package.find_library)


_hid_list = list()
_vid = 0x483
_pid = 0x5750


def _find_device(serial_number: str) -> usb.core.Device:
	if serial_number == '':
		dev = usb.core.find(idVendor=_vid, idProduct=_pid, backend=_backend)
	else:
		dev = usb.core.find(idVendor=_vid, idProduct=_pid, serial_number=serial_number, backend=_backend)

	return dev


def list_serial_numbers():
	dev_all = usb.core.find(find_all=True, idVendor=_vid, idProduct=_pid, manufacturer='Kersci', product='HIDSerial')
	serial_numbers = []
	for dev in dev_all:
		serial_numbers.append(dev.serial_number)
	return serial_numbers


class Serial:
	def __init__(self, port: str, baudrate: int, timeout: float = 0):
		dev_type, serial_nb_raw, name = port.split('::')
		assert dev_type.lower() == 'uhserial', f'Device type "{dev_type}" not supported.'
		assert name[0] in 'Ss', f'Device name must be "Sxxx" format, where "xxx" are decimal digit(s).'
		try:
			index = int(name[1:])
		except IndexError:
			raise ValueError(f'Device name must be "Sxxx" format, where "xxx" are decimal digit(s).')
		except ValueError:
			raise ValueError(f'Device name must be "Sxxx" format, where "xxx" are decimal digit(s).')
		assert 0 < index < 8, f'Device index "{name}" out of range.'

		serial_nb: str = serial_nb_raw.lower()
		if serial_nb == 'any':
			serial_nb = ''
		dev = _find_device(serial_nb)
		if dev is None:
			if serial_nb:
				raise ValueError(f'UHSerial with serial number "{serial_nb_raw}" not found.')
			else:
				raise ValueError('No UHSerial device found.')


if __name__ == '__main__':
	serials = list_serial_numbers()
	output = ', '.join(serials)
	print(output)
