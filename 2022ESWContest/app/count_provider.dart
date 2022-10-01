import 'package:flutter/foundation.dart';

class CountProvider extends ChangeNotifier{
  double _volume =1.0;
  double _pitch = 1.0;
  double _speechRate = 0.5;

  double get volume => _volume;
  double get pitch => _pitch;
  double get speechRate => _speechRate;

  set volume(double value) {
    _volume = value;
    notifyListeners();
  }

  set pitch(double value) {
    _pitch = value;
    notifyListeners();
  }

  set speechRate(double value) {
    _speechRate = value;
    notifyListeners();
  }
}
