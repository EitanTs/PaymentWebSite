

function setSubmit(flag)
{
    if (document.getElementById("submit") != null)
        document.getElementById("submit").disabled = flag
}


function validInputById(name)
{
    if (document.getElementById(name) == null) {
        return true
    }
    return document.getElementById(name).value.length > 0
}

function validAllInputs()
{
    
    var names = ["Name", "AmountPayed", "Hours", "Debt"]
    for (var i = 0; i < names.length; i++)
    {
        if (!validInputById(names[i]))
        {
            setSubmit(true)
            return
        }
    }
    setSubmit(false)
}

