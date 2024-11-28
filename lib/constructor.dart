class Constructor {
  static String username = "";
  static bool isListening = false;
  static String userMessage = "";
  static String botResponse = "Bot: Chào bạn! Hãy nói điều gì đó...";
  static bool isLoading = false;
  static List<Map<String, dynamic>> messages = [];

  static Function(String)? onUserMessageChanged;
  static Function(String)? onBotResponseChanged;
  static Function(bool)? onLoadingChanged;

  static void updateUserMessage(String message) {
    userMessage = message;
    if (onUserMessageChanged != null) {
      onUserMessageChanged!(message);
    }
  }

  static void updateBotResponse(String response) {
    botResponse = response;
    if (onBotResponseChanged != null) {
      onBotResponseChanged!(response);
    }
  }

  static void updateLoading(bool loading) {
    isLoading = loading;
    if (onLoadingChanged != null) {
      onLoadingChanged!(loading);
    }
  }
}
