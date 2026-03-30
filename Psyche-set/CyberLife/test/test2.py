

hey = { 
    "cheese": 'cheese',
    "emotion": {
        'happy': {
            'numpy': 4
        }
    }
}
ex = ['happy']
jj = list(hey.get('emotion', 0).keys())[0]
print(jj)
test = ['emotion'][jj]
h = hey[test]
print(h)