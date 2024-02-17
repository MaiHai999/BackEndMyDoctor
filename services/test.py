from underthesea import classify

while True:
    text = input("Nhập đoạn văn bản của bạn: ")
    a = classify(text)
    print(a)