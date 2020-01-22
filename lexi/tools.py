def open_file(txt_file_path):
    txtFile = open(txt_file_path, "r")
    mostCommonWords = txtFile.read().split(",")
    txtFile.close()
    return mostCommonWords

def set_elapsed_time (elapsed):
    if elapsed > 60:
        elapsed /= 60
        if elapsed > 60:
            return str(round(elapsed/60,2))+" hours"
        else:
            return str(round(elapsed,2))+" minutes"
    else:
        return str(round(elapsed,2))+" seconds"