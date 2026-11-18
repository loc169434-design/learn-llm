# Sổ Tay Kiến Thức & Phỏng Vấn Thực Chiến — DriveSafe AI (Android + AI Backend)

Tài liệu này ghi lại toàn bộ **kiến thức cốt lõi, cơ chế hệ thống, quyết định kiến trúc (Trade-offs) và bộ câu hỏi phỏng vấn Senior** tương ứng với từng Module thực tế xây dựng trong dự án **DriveSafe AI**.

---

## Cấu Trúc Ghi Chép Cho Mỗi Module (Chuẩn Phỏng Vấn Senior)
Mỗi tính năng sau khi code và test chạy thật sẽ được đúc kết theo 4 mục:
1. **Bài toán thực tế (STAR Story):** Tình huống trên xe → Vấn đề kỹ thuật → Giải pháp → Kết quả đo đếm được.
2. **Cơ chế hoạt động bên dưới (Under the Hood):** Luồng chạy thật sự của Android OS / Kotlin Coroutines / FastAPI / Gemini LLM.
3. **Trade-offs (Tại sao chọn A thay vì B?):** Điểm ăn tiền nhất khi phỏng vấn mức Senior.
4. **Câu hỏi phỏng vấn xoáy sâu & Gợi ý trả lời:** Các câu hỏi thực tế hội đồng kỹ thuật sẽ hỏi từ chính đoạn code bạn viết.

---

## Lộ Trình 5 Module Xây Dựng & Tích Lũy Kiến Thức

### [x] Module 1: Production AI Backend — Phân Loại, Gom Tóm Tắt & Chuẩn Hóa Tin Nhắn (`backend/`)

- **Source code:** `backend/app/schemas/drive.py`, `backend/app/services/gemini_service.py`, `backend/app/api/drive_routes.py`, `backend/tests/test_drive_api.py`.

#### 1. STAR Story (Dùng để giới thiệu trong phỏng vấn)
- **Situation & Task:** Khi đang lái ô tô và bật bản đồ dẫn đường, tài xế nhận rất nhiều thông báo Zalo/Messenger dồn dập (4–5 tin ngắn rời rạc xen lẫn tin quảng cáo OA). Cần xây dựng Backend AI lọc bỏ 100% tin rác, gom các tin rời rạc thành 1 câu tự nhiên dưới 30 từ để đọc qua loa, và biên tập lại câu nói thô của tài xế thành tin nhắn lịch sự gửi đi.
- **Action:** Thiết kế Backend FastAPI phân tầng (`api` → `services` → `schemas`), dùng Gemini **Structured Output** (`response_schema` + `temperature=0.0`) ép đầu ra khớp tuyệt đối Pydantic v2 schema, và dùng Dependency Injection (`Depends`) để viết bộ Unit Test Mock chạy trong `0.3s`.
- **Result:** API phản hồi ổn định đúng 100% JSON contract cho App Android, lọc chính xác quảng cáo (`IGNORE_SPAM`), không tốn chi phí token khi chạy CI/CD test.

#### 2. Cơ chế hoạt động bên dưới (Under the Hood)
- **Constrained Decoding trong Structured Output:** Khác với việc chỉ viết prompt *"Hãy trả về JSON"* (LLM vẫn có thể thêm dấu ````json` hoặc sai tên trường làm crash parser trên Android), việc truyền `response_mime_type="application/json"` kèm `response_schema=TriageDecision` ép tầng giải mã token của Gemini chỉ được sinh các token tuân thủ ngữ pháp JSON Schema đó.
- **FastAPI Dependency Injection (`Depends`):** Route handler không khởi tạo cứng `GeminiDriveAiService` bên trong hàm mà nhận qua `service: DriveAiService = Depends(_provide_service)`. Nhờ vậy trong `test_drive_api.py`, chỉ cần gán `app.dependency_overrides[_provide_service] = lambda: MockDriveAiService()` là hoán đổi toàn bộ tầng gọi AI thật sang Mock trong RAM.

#### 3. Trade-offs (Tại sao chọn A thay vì B?)
- **Tại sao gọi Gemini qua Backend FastAPI thay vì gọi trực tiếp SDK trên App Android?**
  1. **Bảo mật API Key:** Nhúng API Key trong APK (dù giấu ở `BuildConfig` hay NDK `.so`) vẫn có thể bị dịch ngược hoặc bắt gói tin lấy cắp quota. Đặt ở Backend giữ kín key hoàn toàn.
  2. **Cập nhật Prompt/Model tức thì (Zero-App-Update):** Khi muốn tinh chỉnh `TRIAGE_SYSTEM_PROMPT` hoặc đổi model mới (ví dụ từ `2.5-flash` sang `flash-lite-latest`), chỉ cần sửa ở Backend mà không bắt user tải bản cập nhật APK trên Play Store.
- **Tại sao tách `Protocol` (`DriveAiService`) thay vì dùng thẳng class `GeminiDriveAiService`?**
  - Tuân thủ nguyên lý **Dependency Inversion (SOLID)**: tầng API không phụ thuộc cứng vào Google Gemini. Ngày mai muốn đổi sang OpenAI hay chạy model local (Ollama/vLLM) chỉ cần viết class mới implement `DriveAiService` mà không sửa 1 dòng nào ở `drive_routes.py`.

#### 4. Câu hỏi phỏng vấn xoáy sâu & Gợi ý trả lời
1. **Hỏi:** *"Làm sao bạn đảm bảo LLM không bịa nội dung hoặc trả sai cấu trúc JSON làm crash app Mobile?"*  
   **Đáp:** Em kết hợp 3 lớp bảo vệ: (1) Dùng `response_schema` (Constrained Decoding) để khóa cứng cấu trúc JSON ở tầng sinh token, (2) Hạ `temperature=0.0` ở bước phân loại (`triage`) để kết quả nhất quán tối đa, và (3) Validate lại một lần nữa bằng Pydantic v2 (`TriageDecision`) tại FastAPI trước khi trả HTTP 200 về Android.
2. **Hỏi:** *"Hệ thống tích hợp LLM khi chạy Unit Test trong CI/CD thường chậm và tốn tiền token, bạn xử lý thế nào?"*  
   **Đáp:** Em tách riêng **Unit Test** và **Integration Test**. Ở Unit Test (`test_drive_api.py`), em dùng `app.dependency_overrides` của FastAPI để inject `MockDriveAiService`, giúp test toàn bộ validation (422), routing, error handling trong `0.3s` với chi phí \$0 và không bao giờ bị flaky do mạng.
3. **Hỏi:** *"Tại sao trong `pyproject.toml` cần cấu hình `pythonpath = [\".\"]` cho `pytest`?"*  
   **Đáp:** Mặc định khi chạy `pytest backend/tests/...`, thư mục gốc của repo đôi khi không tự nằm trong `sys.path`, dẫn đến `ModuleNotFoundError: No module named 'backend'`. Khai báo `pythonpath = ["."]` chuẩn hóa môi trường chạy test đồng nhất trên mọi máy dev và CI.

### [x] Module 2: Android Notification Collector & Coroutine Debouncer (`NotificationListenerService`)

- **Source code (`~/AndroidStudioProjects/DriveSafeAI`):**
  - `automation/notification/CarNotificationListenerService.kt`
  - `automation/notification/NotificationBatchDebouncer.kt` + `NotificationBatchDebouncerTest.kt`
  - `automation/notification/ActiveReplyActionStore.kt`
  - `ui/dashboard/DriveDashboardContract.kt`, `DriveDashboardViewModel.kt`, `DriveDashboardScreen.kt`

#### 1. STAR Story (Dùng để giới thiệu trong phỏng vấn Android Senior)
- **Situation & Task:** Người dùng Zalo tại Việt Nam có thói quen gõ tách thành 3–5 tin nhắn ngắn liên tiếp trong vài giây. Nếu đọc từng notification ngay khi `onNotificationPosted` nổ thì loa xe sẽ ngắt nhạc liên tục gây ức chế; đồng thời Zalo còn bắn kèm 1 notification tổng hợp (`FLAG_GROUP_SUMMARY`) làm bị đọc lặp.
- **Action:** Xây dựng `CarNotificationListenerService` lọc sạch `FLAG_GROUP_SUMMARY` & `isOngoing`, trích xuất sẵn cặp `(PendingIntent, RemoteInput)` lưu vào `ConcurrentHashMap`, và thiết kế `NotificationBatchDebouncer` dùng Coroutines + `Mutex` để gom tin nhắn theo từng người gửi độc lập (cửa sổ 4 giây) kèm khử trùng lặp liên tiếp.
- **Result:** 5 tin nhắn dồn dập của 1 người được gộp gọn thành đúng 1 batch duy nhất sau 4 giây yên ắng; tin nhắn từ 2 người khác nhau không làm trễ timer của nhau; test tự động 100% bằng `kotlinx-coroutines-test` (`VirtualTime`).

#### 2. Cơ chế hoạt động bên dưới (Under the Hood)
- **System-Bound Service:** `NotificationListenerService` không được khởi chạy bằng `startService()` từ app mà do **Android System (`NotificationManagerService`)** tự `bind` qua Binder IPC khi user bật công tắc trong *Notification Access Settings*. Vì vậy trên `AndroidManifest.xml` bắt buộc phải khai báo `android:permission="android.permission.BIND_NOTIFICATION_LISTENER_SERVICE"` để chặn app độc hại bên ngoài giả mạo hệ thống bind vào service.
- **Coroutine Scope trong Service (`SupervisorJob`):** `serviceScope = CoroutineScope(SupervisorJob() + Dispatchers.Default)`. Nếu dùng `Job()` thường, chỉ cần 1 coroutine xử lý thông báo của 1 cuộc hội thoại văng exception là toàn bộ `serviceScope` bị hủy vĩnh viễn cho tới khi khởi động lại Service. `SupervisorJob()` cô lập lỗi của từng coroutine con.
- **Per-Key Debounce với `Mutex`:** Khác với `Flow.debounce(4000)` đơn giản (sẽ làm tin nhắn của "Sếp" reset luôn bộ đếm của "Vợ" nếu dùng chung 1 stream!), `NotificationBatchDebouncer` quản lý `flushJob: Job?` riêng cho từng `conversationKey` bên trong `Mutex.withLock`, đảm bảo không bị Race Condition khi nhiều luồng Binder gọi vào cùng lúc.

#### 3. Trade-offs (Tại sao chọn A thay vì B?)
- **Tại sao dùng `Mutex` của Coroutines thay vì `synchronized` block truyền thống?**
  - `Mutex.withLock` là *suspending* (nhường thread chứ không khóa cứng OS thread như `synchronized`), an toàn và idiomatic hơn khi kết hợp với `Dispatchers.Default` và `runTest` trong Coroutines.
- **Tại sao kiểm tra quyền lại nằm trong `Lifecycle.Event.ON_RESUME` (`DisposableEffect`) trên Compose?**
  - Quyền `Notification Access` không có popup runtime `ActivityResultContracts.RequestPermission` mà phải mở màn hình Settings hệ thống (`ACTION_NOTIFICATION_LISTENER_SETTINGS`). Khi user gạt nút bật rồi bấm Back quay về app, sự kiện `ON_RESUME` tự động kích hoạt `NotificationManagerCompat.getEnabledListenerPackages(context)` cập nhật `UiState` xanh ngay lập tức mà không cần user bấm refresh.

#### 4. Câu hỏi phỏng vấn xoáy sâu & Gợi ý trả lời
1. **Hỏi:** *"Làm sao test hàm có `delay(4000L)` trong Unit Test mà không bắt CI phải ngồi chờ thật 4 giây mỗi test?"*  
   **Đáp:** Em truyền `CoroutineScope` từ ngoài vào `NotificationBatchDebouncer` (Dependency Injection). Trong `NotificationBatchDebouncerTest`, em dùng `runTest` + `backgroundScope` của `kotlinx-coroutines-test` sử dụng đồng hồ ảo (*Virtual Time Scheduler*), dùng `advanceTimeBy(3_999L)` và `advanceTimeBy(1L)` kiểm chứng chính xác từng mili-giây mà test chạy xong chỉ mất `0.02s`.
2. **Hỏi:** *"Khi biên dịch gặp lỗi AAR Metadata báo thư viện AndroidX yêu cầu `compileSdk 37` trong khi máy khách hàng chạy Android 10 (`API 29`), nâng `compileSdk = 37` có làm app crash trên máy Android 10 không?"*  
   **Đáp:** Không hề ảnh hưởng. `compileSdk` chỉ quyết định phiên bản SDK dùng lúc biên dịch (giúp trình biên dịch hiểu các API/annotation mới trong thư viện Jetpack), còn thiết bị cài được quyết định bởi `minSdk = 26` và hành vi runtime quyết định bởi `targetSdk`.

### [x] Module 3: Silent Reply Automation & Audio Ducking (`RemoteInput` + `AudioFocusRequest`)

- **Source code (`~/AndroidStudioProjects/DriveSafeAI`):**
  - `automation/audio/CarSpeechSpeaker.kt` (`TextToSpeech` + `AudioFocusRequest` + `suspendCancellableCoroutine`)
  - `automation/audio/CarVoiceRecognizer.kt` (`SpeechRecognizer` trên `Dispatchers.Main.immediate`)
  - `automation/reply/SilentReplySender.kt` (`RemoteInput` + `PendingIntent` IPC)

#### 1. STAR Story (Dùng để giới thiệu trong phỏng vấn Android Senior)
- **Situation & Task:** Khi đang lái xe mở Vietmap dẫn đường và bật nhạc Spotify, tài xế cần nghe tin nhắn Zalo rõ ràng mà không làm tắt hẳn nhạc, sau đó trả lời lại bằng giọng nói mà không được bật màn hình Zalo che khuất bản đồ.
- **Action:** Xây dựng `CarSpeechSpeaker` xin quyền âm thanh tạm thời `AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK` gói trong `suspendCancellableCoroutine` để nhả focus ngay khi đọc xong câu; dùng `CarVoiceRecognizer` thu giọng nói tiếng Việt `vi-VN`; và dùng `SilentReplySender` bơm câu trả lời vào `RemoteInput` của `PendingIntent` có sẵn trên Notification Zalo.
- **Result:** Nhạc nền tự động hạ nhỏ êm ái trong vài giây đọc tin rồi tự vặn lớn lại; tin nhắn trả lời gửi thẳng đi dưới nền 100% (kể cả khi màn hình khóa hoặc đang full-screen Vietmap).

#### 2. Cơ chế hoạt động bên dưới (Under the Hood)
- **Cơ chế `PendingIntent` + `RemoteInput` qua Binder IPC:** Khi Zalo tạo thông báo có nút *"Trả lời"*, Zalo đăng ký một `PendingIntent` (trỏ tới `BroadcastReceiver` nội bộ của Zalo) trong bảng `ActivityManagerService` của hệ thống kèm khóa `RemoteInput.resultKey`. Khi DriveSafe AI gọi `RemoteInput.addResultsToIntent(...)` và `actionIntent.send(context, 0, fillInIntent)`, System Server chuyển `ClipData` chứa câu trả lời qua Binder sang thẳng tiến trình của Zalo với đúng quyền định danh của Zalo — không cần bất kỳ thao tác chạm UI nào.
- **Chuyển Callback sang Coroutine (`suspendCancellableCoroutine`):** `TextToSpeech` dùng callback bất đồng bộ `UtteranceProgressListener`. Bằng cách bọc vào `suspendCancellableCoroutine` kèm khối `try / finally { audioManager.abandonAudioFocusRequest(focusRequest) }`, dù đọc thành công, lỗi hay coroutine bị cancel giữa chừng thì `AudioFocus` luôn được trả lại cho Spotify 100%, không bao giờ gây lỗi "kẹt nhỏ tiếng nhạc".
- **Package Visibility trên Android 11+ (`<queries>`):** Từ API 30, nếu không khai báo `<queries>` cho `android.speech.RecognitionService` và `android.intent.action.TTS_SERVICE` trong `AndroidManifest.xml`, hàm `SpeechRecognizer.isRecognitionAvailable(context)` có thể trả về `false` dù máy có cài sẵn Google Speech Services.

#### 3. Trade-offs (Tại sao chọn A thay vì B?)
- **Tại sao ưu tiên `RemoteInput` thay vì dùng `AccessibilityService` tự mở Zalo, tìm ô `EditText` và bấm nút Gửi?**
  1. **An toàn khi lái xe:** `AccessibilityService` bắt buộc phải mở màn hình Zalo đè lên bản đồ Vietmap trong 2–3 giây — cực kỳ nguy hiểm khi tài xế sắp rẽ ở ngã tư. `RemoteInput` chạy ngầm 100%, bản đồ giữ nguyên.
  2. **Độ bền (Zero Fragility):** Nếu Zalo cập nhật phiên bản đổi ID của nút Gửi hoặc đổi cấu trúc layout, `AccessibilityService` gãy ngay lập tức. Còn `RemoteInput` là chuẩn Android Notification API (Android Wear / Android Auto cũng dùng chính cơ chế này) nên không bao giờ vỡ khi Zalo đổi giao diện.
  3. **Chính sách Google Play:** Xin quyền `AccessibilityService` bị Google xét duyệt cực gắt và dễ bị từ chối hoặc cảnh báo bảo mật trên Android 13+, trong khi `NotificationListenerService` cho ứng dụng hỗ trợ lái xe rảnh tay hoàn toàn hợp lệ.

#### 4. Câu hỏi phỏng vấn xoáy sâu & Gợi ý trả lời
1. **Hỏi:** *"Tại sao trong `CarVoiceRecognizer` bạn bắt buộc dùng `Dispatchers.Main.immediate` khi gọi `SpeechRecognizer`?"*  
   **Đáp:** Tài liệu chính thức của Android quy định mọi phương thức của `SpeechRecognizer` (`createSpeechRecognizer`, `startListening`, `stopListening`, `destroy`) bắt buộc phải gọi trên **Main Thread**, nếu gọi từ background thread sẽ ném `RuntimeException`. Dùng `Dispatchers.Main.immediate` đảm bảo an toàn luồng và chạy ngay lập tức không tốn thêm 1 vòng post vào `Looper` nếu đang ở Main Thread sẵn.
2. **Hỏi:** *"Trên Android 14–16 (`API 34+`), việc bắn `PendingIntent` từ nền có thay đổi gì cần lưu ý?"*  
   **Đáp:** Từ Android 14 (API 34), hệ thống chặn mặc định quyền khởi chạy nền của `PendingIntent` (*Background Activity Launch restrictions*). Để đảm bảo `PendingIntent` của app nhắn tin luôn được phép chạy phản hồi, cần truyền `ActivityOptions.makeBasic().setPendingIntentBackgroundActivityStartMode(...)` (`MODE_BACKGROUND_ACTIVITY_START_ALLOW_ALWAYS` trên API 36+) vào hàm `PendingIntent.send(...)`.
3. **Hỏi:** *"Điều gì xảy ra nếu người dùng đã vuốt xóa thông báo Zalo trên thanh trạng thái rồi mới bấm gửi trả lời?"*  
   **Đáp:** Thứ nhất, `onNotificationRemoved` trong `CarNotificationListenerService` đã chủ động xóa handle khỏi `ActiveReplyActionStore`. Thứ hai, ngay cả khi race condition xảy ra và `PendingIntent` vừa bị hủy, `SilentReplySender` bắt `PendingIntent.CanceledException`, dọn sạch cache và trả về `Result.failure` rõ ràng thay vì làm crash ứng dụng.

### [ ] Module 4: MVI Dashboard, Kết Nối Máy Thật (`adb reverse`) & Bluetooth Zero-Touch
- **Code thực chiến:** UI Jetpack Compose theo MVI (`UiState`, `Intent`, `Effect`), Retrofit + OkHttp nối Backend, `BluetoothReceiver` + `ForegroundService` (`connectedDevice` chuẩn Android 14) tự bật chế độ lái & phóng Vietmap khi lên xe.
- **Trọng tâm phỏng vấn Android Senior:**
  - Unidirectional Data Flow (UDF) trong MVI giải quyết lỗi *State Hoisting / Configuration Change* ra sao?
  - Quy định ngặt nghèo của Android 12–14 về khởi chạy `ForegroundService` từ nền (`BackgroundStartNotAllowedException`) và quyền `BLUETOOTH_CONNECT`.

### [ ] Module 5: Mở Rộng AI Agent — Tool Calling & RAG Sổ Tay Xe + Docker
- **Code thực chiến:** Function Calling ghi nhận chi phí xăng/bảo dưỡng + Vector DB (RAG) tra cứu đèn báo lỗi taplo qua SSE Streaming + Dockerize Backend.
- **Trọng tâm phỏng vấn AI Engineer:**
  - Luồng chạy của **Function Calling / Agent Loop** (Model không tự chạy hàm mà trả JSON yêu cầu App/Backend chạy hàm rồi đút kết quả lại).
  - Pipeline **RAG** (Chunking → Embedding → Vector Search → Rerank/Prompting) chống ảo giác như thế nào?
