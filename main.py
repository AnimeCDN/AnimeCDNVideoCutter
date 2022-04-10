#coding=utf-8
import os
import subprocess
import re


def get_length(filename):
    result = subprocess.Popen(["ffprobe", filename],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    for x in result.stdout.readlines():
        if b"Duration" in x:
            print(x)
            x = re.search(rb"Duration.+?\d{2}:(\d{2}):\d{2}", x)
            return int(x.group(1))

def run_cmd(cmd_str='', echo_print=1):
    """
    执行cmd命令，不显示执行过程中弹出的黑框
    备注：subprocess.run()函数会将本来打印到cmd上的内容打印到python执行界面上，所以避免了出现cmd弹出框的问题
    :param cmd_str: 执行的cmd命令
    :return:
    """
    print(cmd_str)
    from subprocess import run
    if echo_print == 1:
        print('\n执行cmd指令="{}"'.format(cmd_str))
    run(cmd_str, shell=True)

def file_name(file_dir):
    File_Name = []
    for files in os.listdir(file_dir):
        if os.path.splitext(files)[1] == '.mp4':
            File_Name.append(files)
    return File_Name


dir = input("请输入mp4文件路径：")
mp4_file_name = file_name(dir)
print("查找到：", mp4_file_name)
for file in mp4_file_name:
    yuan_file_name = file.replace(".mp4", "")
    ts_dir = dir + "\\" + yuan_file_name
    os.system("mkdir \"" + ts_dir + "\"")
    # print(("ffmpeg -y -i \"" + dir + "\\" + file + "\" -vcodec copy -acodec copy -vbsf h264_mp4toannexb "+ts_dir+"\\output.ts").encode("mbcs").decode("gbk"))
    os.system(("ffmpeg -y -i \"" + dir + "\\" + file + "\" -vcodec copy -acodec copy -vbsf h264_mp4toannexb \""+ts_dir+"\\output.ts\"").encode("mbcs").decode("gbk"))
    # print(("ffmpeg -i "+ts_dir+"\\output.ts -c copy -map 0 -f segment -segment_list "+ts_dir+"\\video.m3u8 -segment_time 300 "+ts_dir+"\\300s_%3d.ts").encode("mbcs").decode("gbk"))
    os.system(("ffmpeg -i \""+ts_dir+"\\output.ts\" -c copy -map 0 -f segment -segment_list \""+ts_dir+"\\video.m3u8\" -segment_time 30 \""+ts_dir+"\\30s_%3d.ts\"").encode("mbcs").decode("gbk"))
    os.remove(ts_dir+"\\output.ts")
