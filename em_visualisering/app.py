"""Tkinter-gränssnittet för EM-visualiseringsprogrammet."""

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from .core import *
from .registry import PROBLEMS
from .modes import mode_options_for_problem, normalize_mode_for_problem
from .unit_scaling import (
    display_scale_by_unit,
    display_scale_for,
    format_display_value,
    selectable_display_scales,
    split_label,
)


class ElectrostaticsApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('EM-visualiseringar (elektrostatik och magnetostatik)')
        self.geometry('1900x820')
        self.minsize(1500, 700)
        self.problem_lookup = {p.name: p for p in PROBLEMS}
        self.current_problem = PROBLEMS[0]
        self.param_vars = {}
        self.param_scales = {}
        self.param_specs = {}
        self.param_unit_vars = {}
        self.param_unit_options = {}
        self._build_layout()
        self._load_problem(self.current_problem.name)

    def _build_layout(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        control = ttk.Frame(self, padding=12)
        control.grid(row=0, column=0, sticky='ns')
        control.columnconfigure(0, weight=1)
        plot_frame = ttk.Frame(self, padding=8)
        plot_frame.grid(row=0, column=1, sticky='nsew')
        plot_frame.rowconfigure(0, weight=0)
        plot_frame.rowconfigure(1, weight=1)
        plot_frame.columnconfigure(0, weight=5)
        plot_frame.columnconfigure(1, weight=3)
        plot_frame.columnconfigure(2, weight=4)
        ttk.Label(control, text='Uppgift', font=('TkDefaultFont', 11, 'bold')).grid(row=0, column=0, sticky='w')
        self.problem_var = tk.StringVar(value=self.current_problem.name)
        problem_combo = ttk.Combobox(control, textvariable=self.problem_var, values=[p.name for p in PROBLEMS], state='readonly', width=38)
        problem_combo.grid(row=1, column=0, sticky='ew', pady=(4, 10))
        problem_combo.bind('<<ComboboxSelected>>', lambda e: self._load_problem(self.problem_var.get()))
        ttk.Label(control, text='Visningsläge', font=('TkDefaultFont', 11, 'bold')).grid(row=2, column=0, sticky='w')
        self.mode_display_to_internal = {}
        self.mode_var = tk.StringVar(value='Fält')
        self.mode_combo = ttk.Combobox(control, textvariable=self.mode_var, state='readonly', width=24)
        self.mode_combo.grid(row=3, column=0, sticky='w', pady=(4, 10))
        self.mode_combo.bind('<<ComboboxSelected>>', lambda _event: self.refresh_plot())
        self.desc_label = ttk.Label(control, text='', wraplength=360, justify='left')
        self.desc_label.grid(row=4, column=0, sticky='ew', pady=(0, 10))
        ttk.Label(control, text='Fysikalisk idé', font=('TkDefaultFont', 11, 'bold')).grid(row=5, column=0, sticky='w')
        self.help_label = ttk.Label(control, text='', wraplength=360, justify='left')
        self.help_label.grid(row=6, column=0, sticky='ew', pady=(4, 12))
        ttk.Label(control, text='Parametrar', font=('TkDefaultFont', 11, 'bold')).grid(row=7, column=0, sticky='w')
        self.params_frame = ttk.Frame(control)
        self.params_frame.grid(row=8, column=0, sticky='ew', pady=(6, 12))
        self.params_frame.columnconfigure(1, weight=1)
        ttk.Button(control, text='Rita', command=self.refresh_plot).grid(row=9, column=0, sticky='ew', pady=(0, 6))
        ttk.Button(control, text='Återställ standardvärden', command=self.reset_defaults).grid(row=10, column=0, sticky='ew')
        ttk.Button(control, text='Kontrollera formel/gränsfall', command=self.run_current_check).grid(row=11, column=0, sticky='ew', pady=(6, 0))
        ttk.Label(control, text='Aktuell beräkning', font=('TkDefaultFont', 11, 'bold')).grid(row=12, column=0, sticky='w', pady=(14, 0))
        self.result_label = ttk.Label(control, text='', wraplength=360, justify='left')
        self.result_label.grid(row=13, column=0, sticky='ew', pady=(4, 0))
        info = ('Tips: välj visningsenhet, ändra parametrar och tryck Enter eller Rita. '
                'Enhetsbyten påverkar bara presentationen; beräkningen använder SI.')
        ttk.Label(control, text=info, wraplength=360, justify='left').grid(row=14, column=0, sticky='ew', pady=(18, 0))
        ttk.Label(plot_frame, text='Huvudgraf', font=('TkDefaultFont', 11, 'bold')).grid(row=0, column=0, sticky='w', padx=(0, 4))
        ttk.Label(plot_frame, text='Geometriskiss', font=('TkDefaultFont', 11, 'bold')).grid(row=0, column=1, sticky='w', padx=(4, 4))
        ttk.Label(plot_frame, text='3-D-vy', font=('TkDefaultFont', 11, 'bold')).grid(row=0, column=2, sticky='w', padx=(4, 0))
        self.figure = Figure(figsize=(7.0, 6.0), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky='nsew', padx=(0, 4))
        self.geometry_figure = Figure(figsize=(3.5, 6.0), dpi=100)
        self.geometry_canvas = FigureCanvasTkAgg(self.geometry_figure, master=plot_frame)
        self.geometry_canvas.get_tk_widget().grid(row=1, column=1, sticky='nsew', padx=(4, 4))
        self.view3d_figure = Figure(figsize=(4.5, 6.0), dpi=100)
        self.view3d_canvas = FigureCanvasTkAgg(self.view3d_figure, master=plot_frame)
        self.view3d_canvas.get_tk_widget().grid(row=1, column=2, sticky='nsew', padx=(4, 0))
        self.status_var = tk.StringVar(value='Klar')
        ttk.Label(self, textvariable=self.status_var, anchor='w', relief='sunken', padding=(8, 2)).grid(row=1, column=0, columnspan=2, sticky='ew')

    def _load_problem(self, problem_name):
        self.current_problem = self.problem_lookup[problem_name]
        self.desc_label.configure(text=self.current_problem.description)
        self.help_label.configure(text=self.current_problem.pedagogical_note())
        self.result_label.configure(text='')
        for child in self.params_frame.winfo_children():
            child.destroy()
        self.param_vars.clear()
        self.param_scales.clear()
        self.param_specs.clear()
        self.param_unit_vars.clear()
        self.param_unit_options.clear()
        defaults = self.current_problem.defaults()

        for i, spec in enumerate(self.current_problem.parameter_specs()):
            key = spec.key
            default_value_si = float(defaults[key])
            self.param_specs[key] = spec
            text_label, _unit = split_label(spec.label)
            ttk.Label(self.params_frame, text=text_label).grid(
                row=i, column=0, sticky='w', pady=3, padx=(0, 6)
            )

            if spec.control == 'select':
                labels = list(spec.choice_map)
                selected = min(labels, key=lambda label: abs(spec.choice_map[label] - default_value_si))
                var = tk.StringVar(value=selected)
                widget = ttk.Combobox(
                    self.params_frame,
                    textvariable=var,
                    values=labels,
                    state='readonly',
                    width=18,
                )
                widget.grid(row=i, column=1, sticky='ew', pady=3)
                widget.bind('<<ComboboxSelected>>', lambda _event: self.refresh_plot())
                ttk.Label(self.params_frame, text='').grid(row=i, column=2, sticky='w')
                self.param_vars[key] = var
                continue

            scales = selectable_display_scales(
                spec.label, spec.default_si, spec.display_units
            )
            preferred = display_scale_for(spec.label, default_value_si)
            units = [scale.display_unit for scale in scales]
            selected_unit = preferred.display_unit if preferred.display_unit in units else units[0]
            scale = display_scale_by_unit(spec.label, selected_unit)
            var = tk.StringVar(value=format_display_value(scale.to_display(default_value_si)))

            min_display = scale.to_display(spec.ui_minimum_si) if spec.ui_minimum_si is not None else None
            max_display = scale.to_display(spec.ui_maximum_si) if spec.ui_maximum_si is not None else None
            step_display = spec.step_si / scale.factor if spec.step_si is not None else None
            if spec.control == 'slider' and min_display is not None and max_display is not None:
                widget = ttk.Spinbox(
                    self.params_frame,
                    textvariable=var,
                    from_=min_display,
                    to=max_display,
                    increment=step_display or 0.1,
                    width=18,
                )
            else:
                widget = ttk.Entry(self.params_frame, textvariable=var, width=18)
            widget.grid(row=i, column=1, sticky='ew', pady=3)
            widget.bind('<Return>', lambda _event: self.refresh_plot())

            unit_var = tk.StringVar(value=selected_unit)
            if len(units) > 1:
                unit_widget = ttk.Combobox(
                    self.params_frame,
                    textvariable=unit_var,
                    values=units,
                    state='readonly',
                    width=8,
                )
                unit_widget.grid(row=i, column=2, sticky='w', pady=3, padx=(6, 0))
                unit_widget.bind(
                    '<<ComboboxSelected>>',
                    lambda _event, parameter_key=key: self._change_parameter_unit(parameter_key),
                )
            else:
                ttk.Label(self.params_frame, text=selected_unit).grid(
                    row=i, column=2, sticky='w', pady=3, padx=(6, 0)
                )

            self.param_vars[key] = var
            self.param_scales[key] = scale
            self.param_unit_vars[key] = unit_var
            self.param_unit_options[key] = units

        mode_options = mode_options_for_problem(self.current_problem)
        self.mode_display_to_internal = dict(mode_options)
        self.mode_combo.configure(values=[label for label, _internal in mode_options])
        self.mode_var.set(mode_options[0][0])
        self.refresh_plot()

    def _change_parameter_unit(self, key):
        try:
            old_scale = self.param_scales[key]
            display_value = float(self.param_vars[key].get().replace(',', '.'))
            value_si = old_scale.to_si(display_value)
            new_unit = self.param_unit_vars[key].get()
            new_scale = display_scale_by_unit(self.param_specs[key].label, new_unit)
            self.param_scales[key] = new_scale
            self.param_vars[key].set(format_display_value(new_scale.to_display(value_si)))
        except Exception as exc:
            messagebox.showerror('Fel vid enhetsbyte', str(exc))

    def reset_defaults(self):
        defaults = self.current_problem.defaults()
        for key, var in self.param_vars.items():
            spec = self.param_specs[key]
            if spec.control == 'select':
                mapping = spec.choice_map
                var.set(min(mapping, key=lambda label: abs(mapping[label] - defaults[key])))
                continue
            scale = self.param_scales[key]
            var.set(format_display_value(scale.to_display(defaults[key])))
        self.refresh_plot()

    def _read_params(self):
        params = {}
        for key, var in self.param_vars.items():
            spec = self.param_specs[key]
            if spec.control == 'select':
                params[key] = spec.choice_map[var.get()]
                continue
            try:
                display_value = float(var.get().replace(',', '.'))
                value_si = self.param_scales[key].to_si(display_value)
                params[key] = float(round(value_si)) if spec.integer else value_si
            except ValueError as exc:
                raise ValueError(f"Parametern '{key}' måste vara ett tal.") from exc
        return params

    def _validate_params(self, params):
        issues = self.current_problem.validate_all(params)
        errors = [issue.message for issue in issues if issue.severity == 'error']
        warnings = [issue.message for issue in issues if issue.severity == 'warning']
        if errors:
            raise ValueError('\n'.join(errors))
        if warnings:
            self.status_var.set('Varning: ' + ' '.join(warnings))
        return warnings

    def run_current_check(self):
        try:
            params = self._read_params()
            self._validate_params(params)
            text = self.current_problem.physics_check(params)
            self.result_label.configure(text=text)
            self.status_var.set(f'Kontrollerad: {self.current_problem.name}')
        except Exception as exc:
            self.status_var.set(f'Fel: {exc}')
            messagebox.showerror('Fel vid kontroll', str(exc))

    def refresh_plot(self):
        try:
            params = self._read_params()
            warnings = self._validate_params(params)
            requested_mode = self.mode_display_to_internal.get(self.mode_var.get(), 'Field')
            normalized_mode = normalize_mode_for_problem(self.current_problem, requested_mode)
            self.current_problem.plot(self.figure, params, normalized_mode)
            self.figure.tight_layout()
            self.canvas.draw()
            self.current_problem.draw_geometry(self.geometry_figure, params)
            self.geometry_figure.tight_layout()
            self.geometry_canvas.draw()
            self.current_problem.draw_3d(self.view3d_figure, params, normalized_mode)
            self.view3d_figure.tight_layout()
            self.view3d_canvas.draw()
            self.result_label.configure(text=self.current_problem.result_summary(params, normalized_mode))
            if not warnings:
                self.status_var.set(f'Ritad: {self.current_problem.name} — {self.mode_var.get()}')
        except Exception as exc:
            self.status_var.set(f'Fel: {exc}')
            messagebox.showerror('Fel vid plottning', str(exc))
