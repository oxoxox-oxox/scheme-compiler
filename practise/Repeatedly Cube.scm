(define (repeatedly-cube n x)
   (if (zero? n)
   x
   (begin
        (define (y n x)
        (if (= n 0)
        1
       (* x x x (y (- n 1) x) )
            )
        ) )
            (y n x)
       )
)