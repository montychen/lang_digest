# MP4视频格式
Mp4格式是一个个Box，其中**moov**存储的是metadata信息，**mdat**存储具体音视频数据信息。**如果无法解析出moov数据，是无法播放该mp4文件的**。而**一般情况下ffmpeg生成moov是在mdat写入完成之后的，即mdat会在moov的前面**,如图：

<img src=res/mp4.png alt="mp4文件结构"/>

### [qtfaststart2](https://github.com/danielyaa5/qtfaststart2) 查看mp4文件moov的位置
```bash
# 先安装
pip install qtfaststart2

# 查看 moov的位置
qtfaststart2 -l a.mp4
```
注意：这里用的是 **qtfaststart2**(中间没有 **-** ) 不是 **qt-faststart**， **qt-faststart**不能查看moov的位置，下面有介绍。qtfaststart2 -l a.mp4  命令输出如下：
<pre>
$ qtfaststart2 -l a.mp4
    ftyp (32 bytes)
    moov (8311 bytes)  <--可以看到这个mp4文件的 moov 位置不在后面 
    free (8 bytes)
    mdat (11154820 bytes)
</pre>


### 秒开一： `moov`移前可加快mp4播放、但还是比不上`m3u8`
MP4文件在播放时，ftyp与moov需同时加载完成后，并下载部分mdat的帧数据后，才能开始播放。在播放moov在后面的MP4时，会严重影响用户体验，因为需要加载整个视频，才能获得moov信息后，视频才能播放。针对这种情况，通用的做法是在服务端做处理。**通过ffmpeg命令吧moov移动到mdat前面， 这样视频可以尽快播放，而不用等到整个视频加载完（秒开）**

#### 1. 使用ffmpeg把moov前移
```bash
 ffmpeg -i in.mp4 -c copy -f mp4 -movflags faststart out.mp4
```
-  **`-c copy`** (或者 **`-codec copy`**) 选项表示复制音视频数据，不做任何编码或转码。需要注意的是，-codec copy选项只适用于输入文件和输出文件的编解码格式相同的情况。如果你需要将一个编码格式不同的音视频文件复制为另一种编码格式，需要使用其他的编码器或转码器进行操作。
- **`-f mp4`** 强制指定输入文件的格式是MP4格式

#### 2. qt-faststart把moov前移
**qt-faststart 在安装ffmpeg的时候，会自动安装。** 它是一个由Mike Melanson (melanson@pcisys.net)写的开源程序，是一个命令行工具。你可能可以在很多地方找到它的源码，一般是在FFmpeg的源码中拿，它通常放在FFmpeg源码的tools目录下，比如github仓库中的位置为https://github.com/FFmpeg/FFmpeg/blob/master/tools/qt-faststart.c。该程序只有一个源码文件，很小（不到13KB）

qt-faststart的使用十分简单，其调用格式为：
```bash
# in.mp4文件保持不变， 把in.mp4的moov前移后，并生成新的文件out.mp4
qt-faststart in.mp4  out.mp4
```
mp4文件也可以替换为mov文件，因为这个工具其实最开始是为QuickTime格式视频文件编写的

#### 查看mp4音视频的编码格式
FFmpeg 是一个非常强大的视频处理工具，也可以用来查看视频文件的编码信息。在命令行中输入以下命令：
```bash
ffmpeg -i your.mp4
```
在输出的最后2段可以看到音视频的编码格式
```bash
 ...
 Stream #0:0[0x1](und): Video: h264 (High) (avc1 / 0x31637661)   <--- 视频编码格式
 
 Stream #0:1[0x2](und): Audio: aac (LC) (mp4a / 0x6134706D)      <--- 音频编码格式
```

完整的输出如下：
```bash
(my_python3.10_env) ➜  m3u8 ffmpeg -i xinchen.mp4
    ffmpeg version 5.1.2 Copyright (c) 2000-2022 the FFmpeg developers
    built with Apple clang version 14.0.0 (clang-1400.0.29.202)
    configuration: --prefix=/opt/homebrew/Cellar/ffmpeg/5.1.2 --enable-shared --enable-pthreads --enable-version3 --cc=clang --host-cflags= --host-ldflags= --enable-ffplay --enable-gnutls --enable-gpl --enable-libaom --enable-libbluray --enable-libdav1d --enable-libmp3lame --enable-libopus --enable-librav1e --enable-librist --enable-librubberband --enable-libsnappy --enable-libsrt --enable-libtesseract --enable-libtheora --enable-libvidstab --enable-libvmaf --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxml2 --enable-libxvid --enable-lzma --enable-libfontconfig --enable-libfreetype --enable-frei0r --enable-libass --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-libspeex --enable-libsoxr --enable-libzmq --enable-libzimg --disable-libjack --disable-indev=jack --enable-videotoolbox --enable-neon
    libavutil      57. 28.100 / 57. 28.100
    libavcodec     59. 37.100 / 59. 37.100
    libavformat    59. 27.100 / 59. 27.100
    libavdevice    59.  7.100 / 59.  7.100
    libavfilter     8. 44.100 /  8. 44.100
    libswscale      6.  7.100 /  6.  7.100
    libswresample   4.  7.100 /  4.  7.100
    libpostproc    56.  6.100 / 56.  6.100
    Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'xinchen.mp4':
    Metadata:
        major_brand     : isom
        minor_version   : 512
        compatible_brands: isomiso2avc1mp41
        encoder         : Lavf58.76.100
    Duration: 00:00:56.87, start: 0.000000, bitrate: 15296 kb/s

    视频编码格式 ***********************************************  
    Stream #0:0[0x1](und): Video: h264 (High) (avc1 / 0x31637661), yuv420p(progressive), 720x1280, 15163 kb/s, 30 fps, 30 tbr, 15360 tbn (default)
        Metadata:
        handler_name    : VideoHandler
        vendor_id       : [0][0][0][0]
    音频编码格式 ***********************************************    
    Stream #0:1[0x2](und): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 124 kb/s (default)
        Metadata:
        handler_name    : Core Media Audio
        vendor_id       : [0][0][0][0]
```


# m3u8 
m3u8 文件是 HTTP Live Streaming（**HLS**） 协议的部分内容，而 HLS 是一个由苹果公司提出的基于 HTTP 的流媒体网络传输协议。
HLS 是新一代流媒体传输协议，其基本实现原理为将一个大的媒体文件进行**分片(ts文件）**，将该分片文件资源路径记录于 m3u8 文件（即 **playlist**）内，其中附带一些额外描述（比如该资源的多带宽信息···）。
- ts文件是一种视频切片文件，可以直接播放。

HLS 的工作原理是把整个视频分成一个个小的基于 HTTP 的文件来下载，每次只下载一些。在开始一个流媒体会话时，客户端会下载一个包含元数据的 extended M3U (m3u8) playlist文件，用于寻找可用的媒体流。另外m3u8还可以 根据用户的网络带宽情况，自动为客户端匹配一个合适的码率文件进行播放，从而保证视频的流畅度。

HLS 只请求基本的 HTTP 报文，与实时传输协议（RTP）不同，HLS 可以穿过任何允许 HTTP 数据通过的防火墙或者代理服务器。它也很容易使用内容分发网络来传输媒体流。

#### m3u8播放文件列表（playlist）
m3u8文件是一个播放列表（playlist）索引，ts文件是媒体文件。 例子： 一个out.m3u8 播放文件列表的内容大致如下：
```bash
(my_python3.10_env) ➜  m3u8 cat ts/index.m3u8
    #EXTM3U
    #EXT-X-VERSION:3
    #EXT-X-MEDIA-SEQUENCE:0
    #EXT-X-ALLOW-CACHE:YES
    #EXT-X-TARGETDURATION:17
    #EXTINF:16.733333,
    out-0000.ts
    #EXTINF:16.666667,
    out-0001.ts
    #EXTINF:16.666667,
    out-0002.ts
    #EXTINF:6.866667,
    out-0003.ts
    #EXT-X-ENDLIST
```
对于点播来说，客户端只需按顺序下载上述片段资源，依次进行播放即可。而对于直播来说，客户端需要 定时重新请求 该 m3u8 文件，看下是否有新的片段数据需要进行下载并播放。

## 生成m3u8播放文件列表和小的ts分片文件
#### 一、一个命令直接生成m3u8播放文件列表和ts分片文件
```bash
ffmpeg -i filename.mp4 -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls filename.m3u8

```

#### 二、两步生成 m3u8播放文件列表和ts分片文件
**1. 先把mp4转成一个大的ts文件**
```bash
# h264: h264_mp4toannexb
# h265: hevc_mp4toannexb

# 如果视频是h264
ffmpeg -y -i 11.mp4 -vcodec copy  -vbsf h264_mp4toannexb out.ts

# 如果视频是h265
ffmpeg -y -i 11.mp4 -vcodec copy  -vbsf hevc_mp4toannexb out.ts
```
**2. 将大的ts切成小的ts分片、同时生成m3u8播放文件列表**
```bash
ffmpeg -i out.ts  -c copy -map 0 -f segment -segment_list ts/index.m3u8 -segment_time 15 ts/out-%04d.ts

//-f segment:切片
//-segment_list ：输出切片的m3u8
//-segment_time：每个切片的时间（单位秒）
//out-%04d.ts 生成带4个数字的文件，比如 out-0000.ts  out-0001.ts
```




