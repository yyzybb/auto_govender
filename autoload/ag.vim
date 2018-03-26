func! ag#warn(msg)
    echohl WarningMsg
    echomsg a:msg
    echohl NONE
endfunc

let g:py_dir = fnamemodify(expand('<sfile>'), ':p:h:gs?\\?/?')

func! ag#dummy()
endfunc

func! ag#onSave()
    let s:abs_filename = expand('%:p')
    exec(':pyf ' . g:py_dir . '/ag.py')
endfunc
