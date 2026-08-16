rule ClayRat_Android_RAT
{
    meta:
        description = "ClayRat Android RAT - trojanized Grok/xAI client (io.system.system903)"
        family = "ClayRat"
        package = "io.system.system903"
        c2 = "packwatheboss.lol, 193.111.117.72:8080, 91.210.168.138:80"
        ua = "ClayApp/1.0"
        author = "XMask lab"
        date = "2026-08-16"

    strings:
        // package name UTF-16LE (resources.arsc is Stored)
        $pkg16 = { 69 00 6F 00 2E 00 73 00 79 00 73 00 74 00 65 00 6D 00 2E 00 73 00 79 00 73 00 74 00 65 00 6D 00 39 00 30 00 33 }
        // ASCII markers (widzoczne gdy classes.dex jest Stored / po rozpakowaniu)
        $amuv = "com.amuvvoafs"
        $grok = "openSuperGrok"
        $grok2 = "setImagineAutoGenerateVideo"
        $acc = "AppHighlightAccessibilityService"
        $ws = "WebSocketForegroundService"
        $lock = "FakeLockActivity"

    condition:
        $pkg16 or ($amuv and $grok) or 3 of ($grok2, $acc, $ws, $lock)
}