(set-logic SLIA)

(synth-fun f ((name String)) String
    ((Start String) (ntString String) (ntInt Int) (ntBool Bool))
    ((Start String (ntString))
    (ntString String (name " " (str.++ ntString ntString) (str.replace ntString ntString ntString) (str.at ntString ntInt) (str.from_int ntInt) (str.substr ntString ntInt ntInt)))
    (ntInt Int (0 1 2 (+ ntInt ntInt) (- ntInt ntInt) (str.len ntString) (str.to_int ntString) (str.indexof ntString ntString ntInt)))
    (ntBool Bool (true false (str.prefixof ntString ntString) (str.suffixof ntString ntString) (str.contains ntString ntString)))))

(declare-var name String)
(constraint (= (f "Nancy FreeHafer") "Nancy"))
(constraint (= (f "Andrew Cencici") "Andrew"))
(constraint (= (f "Jan Kotas") "Jan"))
(constraint (= (f "Mariya Sergienko") "Mariya"))

(check-synth)
