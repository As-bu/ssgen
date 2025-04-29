from textnode import TextType, TextNode

def main():
	TN1 = TextNode('This is some anchor text', TextType.LINK , 'https://www.boot.dev')
	print(TN1)


if __name__ == '__main__':
	main()

