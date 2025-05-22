def fRecursionGuard(uCounter):
  # This will check if a recursion error is imminent by trying to recursively
  # call itself the specified number of times. If that fails, it unwinds the
  # stack and raises a RecursionError. This allows you to detect this and
  # handle it in your code with still sufficient room on the stack to make
  # a certain number of nested calls.
  if uCounter != 0:
    try:
      fRecursionGuard(uCounter - 1);
    except RecursionError:
      raise RecursionError("Recursion detected");
