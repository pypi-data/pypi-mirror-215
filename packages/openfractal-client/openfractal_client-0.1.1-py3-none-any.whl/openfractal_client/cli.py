import typer

app = typer.Typer(help="openfractal-client CLI", add_completion=False)


@app.command()
def dummy():
    pass


@app.command(help="Display the progress for one dataset.")
def progress(
    dataset_name: str = typer.Option(...),
    dataset_type: str = typer.Option("singlepoint"),
    address: str = typer.Option("http://127.0.0.1:7777"),
    username: str = typer.Option("read_user"),
    password: str = typer.Option("read_password"),
):
    from qcportal import PortalClient

    client = PortalClient(
        address=address,
        username=username,
        password=password,
    )

    ds = client.get_dataset(dataset_type=dataset_type, dataset_name=dataset_name)
    ds.print_status()
