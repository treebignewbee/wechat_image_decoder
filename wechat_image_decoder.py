import os
import sys
from typing import List, Tuple

class WeChatImageDecoder:
    def __init__(self):
        self.supported_types = {
            b'\xFF\xD8\xFF': 'jpg',
            b'\x89PNG\r\n\x1a\n': 'png',
            b'II*\x00': 'tif',
            b'MM\x00*': 'tif',
            b'BM': 'bmp'
        }

    def get_image_type(self, data: bytes) -> str:
        for signature, file_type in self.supported_types.items():
            if data.startswith(signature):
                return file_type
        return 'unknown'

    def decode_wechat_image(self, input_file: str) -> Tuple[bool, str]:
        if not input_file.lower().endswith('.dat'):
            return False, f"Skipping non-DAT file: {input_file}"

        try:
            with open(input_file, "rb") as dat_file:
                buffer = bytearray(dat_file.read())

            xor_key = buffer[0] ^ 0xFF
            decoded_buffer = bytearray([b ^ xor_key for b in buffer])
            image_type = self.get_image_type(decoded_buffer)

            if image_type == 'unknown':
                return False, f"Unknown image type for: {input_file}"

            output_file = os.path.splitext(input_file)[0] + '.' + image_type

            with open(output_file, "wb") as out_file:
                out_file.write(decoded_buffer)

            return True, f"Decoded WeChat image {input_file} to {output_file}"
        except Exception as e:
            return False, f"Error processing WeChat image {input_file}: {str(e)}"

    def process_wechat_images_in_directory(self, directory: str) -> List[str]:
        results = []
        for root, _, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)
                success, message = self.decode_wechat_image(full_path)
                results.append(message)
                if success:
                    print(message)
                else:
                    print(f"Warning: {message}", file=sys.stderr)
        return results

    def process_single_wechat_image(self, file_path: str) -> str:
        success, message = self.decode_wechat_image(file_path)
        if success:
            print(message)
        else:
            print(f"Warning: {message}", file=sys.stderr)
        return message

def main():
    if len(sys.argv) != 2:
        print("Usage: python wechat_image_decoder.py <file_or_directory_path>")
        print("Note: This tool will convert WeChat images (.dat files) in the specified file or directory (including subdirectories).")
        sys.exit(1)

    input_path = sys.argv[1]
    decoder = WeChatImageDecoder()

    if os.path.isfile(input_path):
        decoder.process_single_wechat_image(input_path)
    elif os.path.isdir(input_path):
        decoder.process_wechat_images_in_directory(input_path)
    else:
        print(f"Error: {input_path} is not a valid file or directory.")
        sys.exit(1)

if __name__ == "__main__":
    main()
