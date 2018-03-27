func! ag#warn(msg)
    echohl WarningMsg
    echomsg a:msg
    echohl NONE
endfunc

let g:py_dir = fnamemodify(expand('<sfile>'), ':p:h:gs?\\?/?')
let s:is_debug = 0

func! ag#dummy()
endfunc

func! ag#toggleDebug()
    if s:is_debug == 0
        let s:is_debug = 1
    else
        let s:is_debug = 0
    endif
endfunc

func! ag#onSave()
    let s:abs_filename = expand('%:p')
    exec(':pyf ' . g:py_dir . '/ag.py')
endfunc
