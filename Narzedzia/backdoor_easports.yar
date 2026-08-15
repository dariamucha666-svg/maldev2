rule Backdoor_EASports_Go
{
    meta:
        description = "Go backdoor with easports.gg certificate and NetUserAdd API"
        hash = "178cb931cc846c4ac7bbf2370259e8b9f7d8a45459974115818b5c1e608533c4"
        author = "lab"
        date = "2026-08-14"
        reference = "BackdoorLab / main.itnlwdcdwymtd resolver"

    strings:
        // Overlay CN is ASCII in this sample. Go API names in .rdata are ASCII.
        // wide kept for UTF-16 copies / memory scans.
        $cert    = "easports.gg" ascii wide
        $netuser = "NetUserAdd" ascii wide
        $regset  = "RegSetValueExW" ascii wide
        $proc    = "CreateProcessW" ascii wide
        $token   = "DuplicateTokenEx" ascii wide
        $dns     = "DnsQuery_W" ascii wide

    condition:
        uint16(0) == 0x5A4D
        and uint32(uint32(0x3C)) == 0x00004550
        and filesize > 1000000
        and $cert
        and ($netuser or $regset or $proc or $token or $dns)
}
