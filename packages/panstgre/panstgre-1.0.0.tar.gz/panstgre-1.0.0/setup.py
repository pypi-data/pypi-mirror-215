import setuptools as st

st.setup(
    author = "Lin.Shao",
    author_email = "shaolintcl@hotmail.com",
    description = "Use pandas and psycopg2 to access postgreDB",
    url = "",
    name = "panstgre",
    version = "1.0.0",
    packages = st.find_packages("./"),
    install_requires=[
        "pandas>=2.0.1",
        "psycopg2-binary>=2.9.6",
        ]
    )
