import subprocess
import multiprocess as mp
if __name__ == '__main__':
    pool = mp.Pool()

    def process_1():
        while True:
            print("process 2 running...")
            # subprocess.run(["ffmpeg", "-listen", "1", "-i", "rtmp://127.0.0.1:2001/livecmd1/stream", "-c", "copy", "-f", "flv", "rtmp://127.0.0.1:1935/live1/stream"])
            subprocess.run([
                "ffmpeg", "-listen", "1",
                "-i", "rtmp://127.0.0.1:2001/livecmd1/stream",
                "-async", "1",
                "-c:v", "libx264", "-acodec", "copy", "-b:v", "768k", "-vf", "scale=720:trunc(ow/a/2)*2",
                "-tune", "zerolatency", "-preset", "veryfast", "-crf", "23", "-g", "60", "-hls_list_size", "0", "-f",
                "flv", "rtmp://127.0.0.1:1935/hls1/stream_mid",
                "-c:v", "libx264", "-acodec", "copy", "-b:v", "1024k", "-vf", "scale=960:trunc(ow/a/2)*2",
                "-tune", "zerolatency", "-preset", "veryfast", "-crf", "23", "-g", "60", "-hls_list_size", "0", "-f",
                "flv", "rtmp://127.0.0.1:1935/hls1/stream_high",
                "-c:v", "libx264", "-acodec", "copy", "-b:v", "1920k", "-vf", "scale=1280:trunc(ow/a/2)*2",
                "-tune", "zerolatency", "-preset", "veryfast", "-crf", "23", "-g", "60", "-hls_list_size", "0", "-f",
                "flv", "rtmp://127.0.0.1:1935/hls1/stream_higher",
                "-c", "copy", "-f", "flv", "rtmp://127.0.0.1:1935/hls1/stream_src"
            ])
    def process_2():
        while True:
            print("process 1 running...")
            subprocess.run(["ffmpeg", "-listen", "1", "-i", "rtmp://127.0.0.1:2002/livecmd2/stream", "-c", "copy", "-f", "flv", "rtmp://127.0.0.1:1935/live1/stream"])

    result1 = pool.apply_async(process_1, [])    # evaluate "solve1(A)" asynchronously
    result2 = pool.apply_async(process_2, [])    # evaluate "solve2(B)" asynchronously

    outputs1 = result1.get()
    outputs2 = result2.get()


#     exec ffmpeg -i rtmp://localhost/$app/$name  -async 1 -vsync -1
#     -c:v libx264 -acodec copy -b:v 256k -vf "scale=480:trunc(ow/a/2)*2" -tune zerolatency -preset veryfast -crf 23 -g 60 -hls_list_size 0 -f flv rtmp://localhost/hls/$name_low
#     -c:v libx264 -acodec copy -b:v 768k -vf "scale=720:trunc(ow/a/2)*2" -tune zerolatency -preset veryfast -crf 23 -g 60 -hls_list_size 0 -f flv rtmp://localhost/hls/$name_mid
#     -c:v libx264 -acodec copy -b:v 1024k -vf "scale=960:trunc(ow/a/2)*2" -tune zerolatency -preset veryfast -crf 23 -g 60 -hls_list_size 0 -f flv rtmp://localhost/hls/$name_high
#     -c:v libx264 -acodec copy -b:v 1920k -vf "scale=1280:trunc(ow/a/2)*2" -tune zerolatency -preset veryfast -crf 23 -g 60 -hls_list_size 0 -f flv rtmp://localhost/hls/$name_higher
#     -c copy -f flv rtmp://localhost/hls/$name_src;

