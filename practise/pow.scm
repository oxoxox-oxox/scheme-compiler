(define (square n)
    (* n n))

(define (pow base exp)
(if (= exp 0)
        1
    (if (= (remainder exp 2) 0)
        (square (pow base (/ exp 2)))
        (* base (pow base (- exp 1))
)))
)

