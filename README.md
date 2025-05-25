# Chinese Assist (中文学习助手)

Chinese Assist 是一个帮助用户学习中文词汇的Web应用程序。它提供了多种功能，包括词汇管理、听写练习、以及通过图像识别技术添加手写词汇。

## 主要功能

*   **词汇管理**: 用户可以添加、查看词汇列表。
*   **听写功能**: 用户可以进行听写练习，系统会朗读词汇。
*   **词语解释**: 在听写过程中，可以请求当前词汇的解释（使用Gemini API）。
*   **图像词汇识别 (新功能)**: 用户可以上传包含手写中文词汇的图片，系统将尝试识别这些词汇并将其填入词汇输入框。

## 安装与配置

### 1. 获取与配置 Gemini API 密钥

本应用的“词语解释”功能和“图像词汇识别”功能依赖于 Google Gemini API。您需要拥有一个有效的 Gemini API 密钥才能使用这些功能。

*   **获取密钥**: 请访问 [Google AI Studio](https://aistudio.google.com/app/apikey) (或其他相关Google Cloud服务页面) 创建并获取您的 API 密钥。
*   **设置环境变量**: 为了让应用能够访问密钥，您需要将其设置为一个环境变量。推荐的环境变量名称是 `GOOGLE_API_KEY`。
    *   **Linux/macOS**:
        ```bash
        export GOOGLE_API_KEY="您的API密钥"
        ```
        为了永久生效，可以将这行命令添加到您的 `~/.bashrc`, `~/.zshrc` 或其他shell配置文件中。
    *   **Windows**:
        ```powershell
        $Env:GOOGLE_API_KEY="您的API密钥"
        ```
        或者通过系统属性设置环境变量。
    *   **重要提示**: 如果您在 `app.py` 中看到有关 `GOOGLE_API_KEY` 未设置的警告，这意味着应用无法找到API密钥，相关功能将无法正常工作。

### 2. 安装依赖

项目所需的Python包在 `requirements.txt` 文件中列出。请使用以下命令安装它们：

```bash
pip install -r requirements.txt
```
这将安装 Flask (Web框架) 和 google-generativeai (Gemini API客户端库) 等必要的库。

## 使用说明

1.  **启动应用**:
    ```bash
    python app.py
    ```
    应用默认会在 `http://0.0.0.0:8089` 启动。

2.  **访问词汇助手页面 (`/vocabulary`)**:
    *   **手动输入词汇**: 在文本框中输入词汇，用空格分隔，然后点击“提交词汇”。
    *   **通过图像识别添加词汇**:
        1.  点击“Choose File”或类似按钮选择一个包含手写中文词汇的图片文件 (支持 .png, .jpg, .jpeg, .gif 格式)。
        2.  点击“Recognize Words from Image”按钮。
        3.  系统将调用 Gemini API 识别图片中的文字。识别完成后，文字会自动填充到上方的词汇输入框中。
        4.  您可以编辑输入框中的词汇，然后点击“提交词汇”将其添加到词汇列表。
        5.  识别状态（如“Recognizing...”, “Recognition complete.”, 或错误信息）会显示在按钮下方。

3.  **进行听写**:
    *   在词汇页面，当词汇列表不为空时，点击“听写”按钮开始。
    *   系统会依次朗读词汇。
    *   可以使用“Pause”/“Resume”按钮暂停或继续听写。
    *   可以点击“Explain Current Word”按钮获取当前朗读词汇的解释。

## 注意事项

*   图像识别的准确性取决于图片质量和手写文字的清晰度。
*   API密钥的安全性非常重要，请勿将其直接硬编码到代码中或公开分享。使用环境变量是推荐的做法。
*   确保您的开发环境中可以访问 Google Gemini API 服务。