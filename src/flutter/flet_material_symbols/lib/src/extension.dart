import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

import 'symbols_icons.dart';

class Extension extends FletExtension {
  @override
  IconData? createIconData(int iconCode) {
    int setId = (iconCode >> 16) & 0xFF;
    int iconIndex = iconCode & 0xFFFF;

    if (setId == 3) {
      if (iconIndex < symbolsIcons.length) {
        return symbolsIcons[iconIndex];
      }
    }

    return null;
  }
}
