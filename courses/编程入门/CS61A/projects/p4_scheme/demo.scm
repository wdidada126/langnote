; demo.scm —— P4 mini-Scheme 示例程序（python scheme.py demo.scm）
; 覆盖：递归/尾递归/闭包/宏/流/coin-count（对应讲义 L07/L19-L23）

(display "hello from mini-Scheme")
(newline)

; ---- 线性递归（L07） ----
(define (fact n) (if (= n 0) 1 (* n (fact (- n 1)))))
(display (fact 20))
(newline)

; ---- 尾递归 10 万步不死（L22 蹦床） ----
(define (sum-to n acc) (if (= n 0) acc (sum-to (- n 1) (+ acc n))))
(display (sum-to 100000 0))
(newline)

; ---- 闭包 = 过程 + 闭合环境（L06/L21） ----
(define (make-adder n) (lambda (k) (+ k n)))
(display ((make-adder 3) 4))
(newline)

; ---- 宏（L22） ----
(define-macro when (pred . rest)
  (cons 'if (cons pred (list (cons 'begin rest)))))
(when (> 1 0)
  (display "macro when works")
  (newline))

; ---- 流与惰性求值（L23） ----
(define (integers-from n) (cons-stream n (integers-from (+ n 1))))
(define (even-stream s) (cons-stream (car s) (even-stream (cdr (cdr s)))))
(display (stream-ref (even-stream (integers-from 1)) 50))   ; 第 51 个偶数=102
(newline)

; ---- SICP 经典 count-change（L07 树递归） ----
(define coins (list 1 5 10 25 50))
(define (first-denomination k) (list-ref coins (- k 1)))
(define (cc amount kinds)
  (cond ((= amount 0) 1)
        ((or (< amount 0) (= kinds 0)) 0)
        (else (+ (cc amount (- kinds 1))
                 (cc (- amount (first-denomination kinds)) kinds)))))
(display (cc 100 5))
(newline)
