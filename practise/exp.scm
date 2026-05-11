(define (exp b n)
  (define (helper n so-far) ;; since b never changes, we can use the b from the outer function
    (if (= n 0)
    so-far
    (helper (- n 1) (* b so-far))
    )
  )
  (helper n 1)
)