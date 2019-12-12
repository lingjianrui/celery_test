from tasks import video_compress, video_upload
if __name__ == '__main__':
    video_compress.apply_async(["a"],queue='tasks', priority=3)
    video_compress.apply_async(["b"],queue='tasks', priority=3)
    video_upload.apply_async(["c"], queue='tasks', priority=2)
    video_upload.apply_async(["d"], queue='tasks', priority=4)
