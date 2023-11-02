# Intercepting TikTok Mobile Requests

Intercepting TikTok requests involves capturing and analyzing network traffic between the app and its servers, providing insights into the app's communication and enabling the automation of every function.


### Understanding TikTok's SSL Pinning:
TikTok implements SSL pinning to enhance security by ensuring that the app only communicates with trusted servers, verified by specific SSL certificates.

Typically, I'll patch the APK using Frida to bypass SSL pinning. However, in this case, patching the APK using Frida isn't necessary since we're using an old Android version.


### Requirements
- [MEmu Emulator](https://www.memuplay.com/)
- [HTTP Toolkit](https://httptoolkit.com/)
- [TikTok APK](https://tiktok.en.uptodown.com/android/post-download)

## Steps:

1. **Launch MEmu Emulator & HTTP Toolkit**

2. **Create a New Android Device in MEmu Emulator**:
   - Create a new virtual Android device with Android version 7.1 (recommended version).
   - In the device settings, enable "Root Device."

3. **Start MEmu then drag & drop the TikTok APK into it to install.**

4. **In HTTP Toolkit, go to the "Intercept" tab and select "Android Device via ADB".**

5. **Open Tiktok & Switch to the "View" tab in HTTP Toolkit to view the requests.**