function clippy()
{
	text = ruleArea.innerText;
	copied = text.createTextRange();
	copied.execCommand("Copy");
}
