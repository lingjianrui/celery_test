from tasks import video_compress, video_upload
if __name__ == '__main__':
    video_compress.apply_async(["a"],queue='highs', priority=8)
    video_compress.apply_async(["b"],queue='low')
    video_upload.apply_async(["c"], queue='low')
    video_upload.apply_async(["d"], queue='highs', priority=1)
