# OpenRGB notes

- Recurring issue: sometimes after reboot, OpenRGB doesn't seem to work.
    - Most common issue: the "size" of some resizeable zones is unknown
        - With OpenRGB GUI open, can see in "show LED mode" that Asteria is sending correct data
        - ...but that isn't being reflect in the LEDs (usually cut off some way).

- Golden settings:
    - Make sure OpenRGB is in "Direct" mode!
        - If not: JRAINBOW1LED1 will set the colour for the whole strip?
    - JRAINBOW1 has 14 LEDs (to confirm: "Rescan devices," set the resizeable zone to be larger than this, then try toggling LED15 on--nothing will happen, but the first 14 will work)
    - Unfixable?: inner LEDs always match the outer ones (probably being fed the same signal?)
    - Check `~/.config/OpenRGB`
        - `OpenRGB.json`: some generic settings? (didn't change anything there; removed it while debugging core dump @ startup)
        - `sizes.ors`: sizes for resizeable zones (can peek a bit with `xxd`; `sizes.ors.bak` was causing core dumps)
        - Also profiles stored here, but not sure what they cover/how they're loaded--might need to adjust systemd unit to pick profile @ startup?


# Packaging notes
- Image in README doesn't show in PyPI (local link doesn't resolve)
    - Could point to `https://gitlab.com/JoshWVS/asteria/-/raw/master/asteria_example.jpg`, but don't love that either?
    - Just host it myself somewhere?

# Systemd notes
- USER UNITS CAN'T DEPEND ON SYSTEM UNITS WHYYYYY https://wiki.archlinux.org/title/Systemd/User (from https://unix.stackexchange.com/questions/147904/systemd-user-unit-that-depends-on-system-unit-sleep-target)
