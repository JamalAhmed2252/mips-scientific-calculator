# Calculator Functions in MIPS Assembly for QtSpim
# Supports: +, -, *, /, power, factorial, sqrt, sin, cos, tan, log

.data
    result: .word 0
    pi: .float 3.141592653589793
    deg_to_rad: .float 0.017453292519943295
    epsilon: .float 0.0001

.text
.globl main

# Addition: $a0 + $a1 -> $v0
add_numbers:
    add $v0, $a0, $a1
    jr $ra

# Subtraction: $a0 - $a1 -> $v0
sub_numbers:
    sub $v0, $a0, $a1
    jr $ra

# Multiplication: $a0 * $a1 -> $v0
mul_numbers:
    mul $v0, $a0, $a1
    jr $ra

# Division: $a0 / $a1 -> $v0
div_numbers:
    div $a0, $a1
    mflo $v0
    jr $ra

# Power: $a0^$a1 -> $v0
power:
    li $v0, 1
    move $t0, $a1
power_loop:
    beqz $t0, power_done
    mul $v0, $v0, $a0
    sub $t0, $t0, 1
    j power_loop
power_done:
    jr $ra

# Factorial: $a0! -> $v0
factorial:
    li $v0, 1
    move $t0, $a0
fact_loop:
    blez $t0, fact_done
    mul $v0, $v0, $t0
    sub $t0, $t0, 1
    j fact_loop
fact_done:
    jr $ra

# Square Root (integer approximation): sqrt($a0) -> $v0
sqrt:
    li $v0, 0
    li $t1, 1
sqrt_loop:
    mul $t2, $t1, $t1
    bgt $t2, $a0, sqrt_done
    move $v0, $t1
    add $t1, $t1, 1
    j sqrt_loop
sqrt_done:
    jr $ra

# Sine approximation (using Taylor series for small angles)
# Input in degrees in $a0, output in $v0 (scaled)
sin_approx:
    # Convert degrees to radians (simplified)
    li $t0, 180
    div $a0, $t0
    mflo $t1        # $t1 = degrees/180
    li $t2, 314     # pi * 100
    mul $a0, $t1, $t2
    
    # Taylor series: sin(x) ≈ x - x^3/6 (for small x)
    move $t0, $a0   # x
    
    # x^3
    mul $t1, $t0, $t0
    mul $t1, $t1, $t0
    
    # x^3/6
    li $t2, 6
    div $t1, $t2
    mflo $t1
    
    # sin(x) = x - x^3/6
    sub $v0, $t0, $t1
    jr $ra

# Cosine approximation
cos_approx:
    # cos(x) = sin(90-x)
    li $t0, 90
    sub $a0, $t0, $a0
    jal sin_approx
    jr $ra

# Tangent approximation
tan_approx:
    # Store $ra
    addiu $sp, $sp, -4
    sw $ra, 0($sp)
    
    # tan(x) = sin(x)/cos(x)
    move $t0, $a0
    
    # Calculate sin(x)
    jal sin_approx
    move $t1, $v0
    
    # Calculate cos(x)
    move $a0, $t0
    jal cos_approx
    move $t2, $v0
    
    # Avoid division by zero
    beqz $t2, tan_error
    div $t1, $t2
    mflo $v0
    j tan_done

tan_error:
    li $v0, 0x7FFFFFFF  # Large number to represent infinity

tan_done:
    lw $ra, 0($sp)
    addiu $sp, $sp, 4
    jr $ra

# Logarithm approximation (base 10)
log_approx:
    li $v0, 0
    li $t0, 10
    move $t1, $a0
log_loop:
    ble $t1, 1, log_done
    div $t1, $t0
    mflo $t1
    add $v0, $v0, 1
    j log_loop
log_done:
    jr $ra

main:
    # This is just to demonstrate the functions
    # The Python frontend will call these functions individually
    jr $ra