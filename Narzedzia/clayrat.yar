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
        $pkg = "io.system.system903"
        $amuv = "com.amuvvoafs"
        $grok1 = "openSuperGrok"
        $grok2 = "setImagineAutoGenerateVideo"
        $grok3 = "setImagineFeedAutoPlay"
        $grok4 = "video_generation_"
        $ws = "WebSocketForegroundService"
        $acc = "AppHighlightAccessibilityService"
        $proj = "MediaProjectionForegroundService"
        $notif = "PushNotificationListenerService"
        $lock = "FakeLockActivity"

    condition:
        $pkg and (($amuv and $grok1) or 4 of ($grok2,$grok3,$grok4,$ws,$acc,$proj,$notif,$lock))
}