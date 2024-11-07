def format_playlist(input_filename, output_filename, encoding="utf-8"):
    """Formats a playlist, handling different file encodings."""
    try:
        with open(input_filename, "r", encoding=encoding) as infile: # Specify encoding
            stations = []
            for line in infile:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    url, image, name = parts
                    name = name.strip().replace("&", "&")
                    stations.append(f"{name},{url},{image}")

        formatted_playlist = "####Stations####\n" + "\n".join(stations)

        with open(output_filename, "w", encoding="utf-8") as outfile: # UTF-8 output
            outfile.write(formatted_playlist)

        return True

    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
        return False
    except UnicodeDecodeError as e:
        print(f"Encoding error: {e}. Try a different encoding (e.g., 'shift_jis' or 'cp932').")
        return False
    except Exception as e:
        print(f"Error processing playlist: {e}")
        return False


# Example usage (try different encodings if needed):
input_file = "radio_data.txt"
output_file = "output_playlist.txt"


if format_playlist(input_file, output_file, encoding="shift_jis"): # Or "cp932"
    print(f"Playlist formatted and saved to '{output_file}'")
elif format_playlist(input_file, output_file, encoding="cp932"):
    print(f"Playlist formatted and saved to '{output_file}' using cp932") # Added for clarity
else:
  print("Could not process file with either encoding.")
# Example usage:
input_file = "radio_data.txt"  # Replace with your input filename
output_file = "output_playlist.txt" # Replace with your desired output filename


if format_playlist(input_file, output_file):
    print(f"Playlist formatted and saved to '{output_file}'")