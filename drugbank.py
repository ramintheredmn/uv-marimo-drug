import marimo

__generated_with = "0.10.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    from rdkit import Chem
    import datamol as dm
    from rdkit.Chem import rdDepictor
    from rdkit.Chem.Draw import rdMolDraw2D
    from rdkit.Chem import Descriptors
    return Chem, Descriptors, dm, mo, pd, rdDepictor, rdMolDraw2D


@app.cell
def _(pd):
    pd.__version__
    return


@app.cell
def _(Chem, Descriptors, rdDepictor, rdMolDraw2D):
    def smitosvg(smi,molSize=(450,150),kekulize=True):
        mol = Chem.MolFromSmiles(smi)
        mc = Chem.Mol(mol.ToBinary())
        if kekulize:
            try:
                Chem.Kekulize(mc)
            except:
                mc = Chem.Mol(mol.ToBinary())
        if not mc.GetNumConformers():
            rdDepictor.Compute2DCoords(mc)
        drawer = rdMolDraw2D.MolDraw2DSVG(molSize[0],molSize[1])
        drawer.DrawMolecule(mc)
        drawer.FinishDrawing()
        svg = drawer.GetDrawingText()
        # It seems that the svg renderer used doesn't quite hit the spec.
        # Here are some fixes to make it work in the notebook, although I think
        # the underlying issue needs to be resolved at the generation step
        return svg.replace('svg:','')
     
    def calc_desk(smi):
        mol = Chem.MolFromSmiles(smi)
        mw = Descriptors.MolWt(mol)
        qed = Descriptors.qed(mol)
        return f"SMILES:{smi}<br>MW:{mw:.2f}<br>qed:{qed:.2f}"
    return calc_desk, smitosvg


@app.cell
def _(mo):
    form = mo.ui.text(label="input SMILES")
    form
    return (form,)


@app.cell
def _(calc_desk, form, mo, smitosvg):
    mo.Html(f"""{smitosvg(form.value)}<br>
    {calc_desk(form.value)}""")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
