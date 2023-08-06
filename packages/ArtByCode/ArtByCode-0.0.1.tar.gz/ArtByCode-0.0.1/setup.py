from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'ArtByCode'
LONG_DESCRIPTION = """
# Welcome to ArtByCode Family

## Description

This is the beginning level python project to do some awesome drawing animation using the `turtle` module, hope it grows in the future

### Usage

- Just install the package `pip install ArtByCode`
- Import it to you project `import ArtByCode` 
- Now you are good to enjoy our arts in our gallery

### Built with

- Turtle 


### Example

```
    from ArtByCode import draw
    
    name = 'lord_ganesh'

    abc(name).draw()
```

### OUTPUT
<div align = "center">
   <img src = "https://github.com/Art-by-Code/Coordinates/assets/114793988/2addc356-8db9-4404-b0ad-2ce0755c3511">
</div>



### Troubleshooting

- If you find any problem, you can contact me on either [insta](https://www.instagram.com/art_by_code?r=nametag)
- You can also find more of my artworks on my youtube channel(https://www.youtube.com/@artbycode)


### Acknowledgements

Thanks to all my followers & friends.❤

### See also

- [Youtube Videos](https://www.youtube.com/@artbycode)
- [My insta ID](https://www.instagram.com/art_by_code?r=nametag)

### Consider supporting me

- Just a simple like, follow & subscribe to our YouTube channel (https://www.youtube.com/@artbycode) and Instagram (https://www.instagram.com/art_by_code?r=nametag) fills our hearts with you warm welcome
- Thanks ❤
"""
# Setting up
setup(
    name="ArtByCode",
    version='0.0.1',
    author="Coder Artist",
    author_email="abc4artbycode@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['turtle==0.0.1', 're', 'docx','requests', 'io'],
    keywords=['python', 'sketch', 'drawing', 'animation',
              'code hub', 'pencil sketch', 'painting'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)