# SimorghOS — per-user language override (set by: simorgh-lang en|fa)
if [ -r "$HOME/.config/simorgh/lang" ]; then
    . "$HOME/.config/simorgh/lang"
    [ -n "$LANG" ] && export LANG
    [ -n "$LANGUAGE" ] && export LANGUAGE
fi
