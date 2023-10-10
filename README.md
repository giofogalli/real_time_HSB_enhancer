# real_time_HSB_enhancer
Real time Hunter-Schreger Bands enhancer from camera.

## Usage
### Select camera index and frame size to be used.
```python
python real_time_HSB_enhancer.py -i 0 -f 1920 1080
```

camera_index [int]: 0, 1, 2 ... <br />
frame_size [int: width height]*: 640 480 (default), 1920 1080, 3840 2160 ... <br />
*it will aprox. to closest camera resolution. <br />

Common resolutions (16:9):<br />
High Definition (HD)    1280 x 720<br />
Full HD, FHD            1920 x 1080<br />
2K, Quad HD, QHD        2560 x 1440<br />
4K, Ultra HD            3840 x 2160<br />
5K, Ultra HD            5120 x 2880<br />
8K, Ultra HD            7680 x 4320<br />

### Real time USB Compliant Camera

Press "c" to change mode between RGB and HSB enhanced.<br />
Press "s" to save current frame in ./saved_frames.<br />
Press "q" or "ESC" to exit.<br />

## Reference
Arrieta, ZL, Fogalli, GB, Line, SRP. Digital enhancement of dental enamel microstructure images from intact teeth. Microsc Res Tech. 2018; 81: 1036–1041. https://doi.org/10.1002/jemt.23070
