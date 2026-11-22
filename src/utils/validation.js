const detailMessage = 'Please describe what happened in a short sentence, for example: “A senior threatened me outside the hostel.” Names and evidence are optional.'

export function descriptionError(value) {
  if ([...value].length > 5000) return 'Please keep your description within 5,000 characters.'
  const letters = value.match(/\p{L}/gu) || []
  if (letters.length < 5 || new Set(letters.map(letter => letter.toLowerCase())).size < 3) return detailMessage
  const words = value.match(/\p{L}[\p{L}\p{M}]*/gu) || []
  const nonLatinScript = letters.some(letter => letter.codePointAt(0) > 0x024f)
  if (!nonLatinScript && words.length < 2) return detailMessage
  if (words.length >= 4 && new Set(words.map(word => word.toLowerCase())).size === 1) return detailMessage
  return ''
}
