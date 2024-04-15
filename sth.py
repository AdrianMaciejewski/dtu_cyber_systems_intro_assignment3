html = """<html>
  <head>
    <title>ESP32 Pins</title>
  </head>
  <body>
    <div class="body-container">
      <h1>ESP32 Pins</h1>
      <div class="table-container">
        <table>
          <thead>
            <tr class="table100-head">
              <th>Pin</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody> %s </tbody>
        </table>
      </div>
    </div>
  </body>
  %s
</html>
"""
style = """
<style>
    * {
      box-sizing: border-box;
      padding: 0px;
      margin: 0px;
    }
    html {
      height: 100%;
    }
    body {
      display: flex;
      justify-content: center;
      height: 100%;
      background: linear-gradient(45deg, #4158d0, #c850c0);
    }
    h1 {
      height: 4rem;
      line-height: 4rem;
      text-align: center;
      color: #eee;
    }
    table {
      border: solid 0px black;
      border-radius: 1rem;
      overflow: hidden;
      border-spacing: 0;
    }
    thead {
      background: #36304a;
    }
    tbody {
      background: #e0e0e0;
    }
    th {
      padding: 0rem 2rem;
      text-align: left;
      font-family: OpenSans-Regular;
      font-size: 18px;
      color: #fff;
      line-height: 1.2;
      font-weight: unset;
    }
    th:first-child
    {
      padding: 0rem 1rem;
    }
    th:last-child
    {
      padding: 0rem 1rem;
    }
    tr {
      border: 0;
      height: 50px;
      padding: 1rem 0rem;
      display: table-row;
      vertical-align: inherit;
      unicode-bidi: isolate;
      border-color: inherit;
    }
    td {
      border: solid 0px black;
      padding: 0rem 2rem;
    }
    td:first-child
    {
      padding: 0rem 1rem;
    }
    th:last-child
    {
      padding: 0rem 1rem;
    }
    .body-container {
      height: 100%;
    }
    .table-container {
      display: flex;
      align-items: center;
      justify-content: center;
    }
  </style>
"""


rows = ['<tr><td>%s</td><td>%d</td></tr>' % (name, pin) for name, pin in {'asdasdsa': 0, 'bbbbbbb': 1, 'vvvv': 0}.items()]
response = html % ('\n'.join(rows), style)
print(response)