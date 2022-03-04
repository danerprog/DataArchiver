
class FailureReason:
    
    YOUTUBE_ARCHIVER = {
        "101" : "Download failed",
        "102" : "Path does not exist",
        "103" : "yt_dlp error caught",
        "104" : "Managed Directory does not exist",
        "105" : "Unable to create needed directories"
    }
    
    def build101(filename):
        return FailureReason.YOUTUBE_ARCHIVER["101"] + ", filename: " + filename
        
    def build102(full_directory, download_url):
        return FailureReason.YOUTUBE_ARCHIVER["102"] + ", full_directory: " + full_directory + ", download_url: " + download_url
        
    def build103(failure_reason):
        return FailureReason.YOUTUBE_ARCHIVER["103"] + ", failure_reason: " + failure_reason
        
    def build104(managed_directory_name):
        return FailureReason.YOUTUBE_ARCHIVER["104"] + ", managed_directory_name: " + managed_directory_name
        
    def build105(error_message):
        return FailureReason.YOUTUBE_ARCHIVER["105"] + ", error_message: " + error_message