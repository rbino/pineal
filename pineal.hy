#!/usr/bin/env hy2

(import [eye [Eye]]
        [ear [Ear]]
        [coder [Coder]])


(defmain [args]
  (setv ths [(Ear) (Eye) (Coder)])

  (for [t ths] (.start t))

  (try
    (while True
      (for [t ths] (.join t 1)))
  (catch [KeyboardInterrupt]
    None))

  (for [t ths] (.stop t)))
